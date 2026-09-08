"""
Aplicação Streamlit: Cockpit Analítico de Segmentação RFM
=========================================================
Interface executiva para diagnóstico da base de clientes, mapeamento de
receita em risco e exportação de listas de ação táticas para CRM e Vendas.

Para executar localmente:
    streamlit run app.py
"""

from datetime import datetime
import io
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from rfm_engine import (
    CLUSTER_METADATA,
    generate_synthetic_transactions,
    calculate_rfm,
    summarize_clusters,
)

# ==============================================================================
# CONFIGURAÇÃO GERAL DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Cockpit Analítico RFM",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ESTILIZAÇÃO CSS CUSTOMIZADA (DESIGN EXECUTIVO MODERNO)
# ==============================================================================
st.markdown(
    """
    <style>
    /* Estilo para cartões de métricas executivas */
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.02) 100%);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(59, 130, 246, 0.4);
    }
    .metric-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        line-height: 1.2;
        color: inherit;
    }
    .metric-subtext {
        font-size: 0.80rem;
        margin-top: 6px;
        color: #64748B;
    }
    .metric-alert {
        border-left: 4px solid #EF4444 !important;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(239, 68, 68, 0.02) 100%);
    }

    /* Cartão de recomendação tática */
    .action-card {
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 6px solid #3B82F6;
        background: rgba(59, 130, 246, 0.04);
        border-top: 1px solid rgba(128, 128, 128, 0.15);
        border-right: 1px solid rgba(128, 128, 128, 0.15);
        border-bottom: 1px solid rgba(128, 128, 128, 0.15);
    }

    /* Badges de prioridade */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-critica { background-color: rgba(239, 68, 68, 0.2); color: #EF4444; }
    .badge-alta { background-color: rgba(245, 158, 11, 0.2); color: #F59E0B; }
    .badge-media { background-color: rgba(59, 130, 246, 0.2); color: #3B82F6; }
    .badge-baixa { background-color: rgba(107, 114, 128, 0.2); color: #9CA3AF; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# FUNÇÕES AUXILIARES DE PROCESSAMENTO DE ARQUIVOS
# ==============================================================================
@st.cache_data(show_spinner=False)
def load_uploaded_file(uploaded_file) -> pd.DataFrame:
    """Lê arquivo CSV ou Excel de forma resiliente."""
    filename = uploaded_file.name.lower()
    if filename.endswith(".csv"):
        # Tenta detectar separador vírgula ou ponto e vírgula
        try:
            df = pd.read_csv(uploaded_file, sep=",")
            if df.shape[1] == 1:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=";")
        except Exception:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, sep=";", encoding="latin1")
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Formato de arquivo não suportado. Utilize CSV ou Excel (.xlsx).")
    return df


def detect_column(columns: list, candidates: list) -> int:
    """Tenta encontrar o índice da melhor coluna correspondente na lista de candidatos."""
    cols_lower = [str(c).lower().strip() for c in columns]
    for candidate in candidates:
        for idx, col in enumerate(cols_lower):
            if candidate == col or candidate in col:
                return idx
    return 0


# ==============================================================================
# SIDEBAR: CONFIGURAÇÕES, UPLOAD E FILTROS
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bullseye.png", width=64)
    st.title("Controle & Dados")
    st.caption("Configurações da base e parâmetros de segmentação.")

    st.markdown("---")
    st.subheader("📂 1. Origem dos Dados")

    data_source = st.radio(
        "Selecione a fonte de dados:",
        options=["🧪 Demonstração (Sintética)", "📁 Upload de Arquivo"],
        index=0,
        help="Use a base sintética realista de 18 meses ou suba sua planilha de transações.",
    )

    raw_df = None

    if data_source == "🧪 Demonstração (Sintética)":
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            n_clients = st.number_input("Clientes:", min_value=100, max_value=5000, value=800, step=100)
        with col_s2:
            n_orders = st.number_input("Transações:", min_value=500, max_value=25000, value=6500, step=500)

        seed_val = st.number_input("Seed (Aleatoriedade):", value=42, step=1)

        if st.button("🔄 Regerar Base Sintética", use_container_width=True):
            st.cache_data.clear()

        with st.spinner("Gerando dados sintéticos com sazonalidade..."):
            raw_df = generate_synthetic_transactions(
                n_customers=int(n_clients),
                n_transactions=int(n_orders),
                seed=int(seed_val),
            )
        st.success(f"Base carregada: {len(raw_df):,} pedidos.")

        col_cli = "id_cliente"
        col_date = "data_transacao"
        col_trx = "id_transacao"
        col_val = "valor_total"

    else:
        uploaded_file = st.file_uploader(
            "Upload de transações (CSV ou Excel)",
            type=["csv", "xlsx", "xls"],
            help="O arquivo deve conter colunas de Cliente, Data da Compra, ID do Pedido e Valor Total.",
        )

        if uploaded_file is not None:
            try:
                raw_df = load_uploaded_file(uploaded_file)
                st.success(f"Arquivo lido com sucesso: {len(raw_df):,} linhas.")
            except Exception as e:
                st.error(f"Erro ao carregar arquivo: {e}")
                st.stop()
        else:
            st.info("Aguardando upload de arquivo ou selecione a base de demonstração acima.")
            st.stop()

        # Mapeamento dinâmico de colunas
        st.markdown("---")
        st.subheader("🔀 2. Mapeamento de Colunas")
        cols_available = list(raw_df.columns)

        def_cli_idx = detect_column(cols_available, ["id_cliente", "cliente", "customer", "client", "cpf", "email"])
        def_date_idx = detect_column(cols_available, ["data_transacao", "data", "date", "created_at", "order_date"])
        def_trx_idx = detect_column(cols_available, ["id_transacao", "pedido", "order", "invoice", "numero_pedido", "id"])
        def_val_idx = detect_column(cols_available, ["valor_total", "valor", "total", "amount", "price", "receita", "faturamento"])

        col_cli = st.selectbox("Coluna de ID Cliente:", cols_available, index=def_cli_idx)
        col_date = st.selectbox("Coluna de Data da Transação:", cols_available, index=def_date_idx)
        col_trx = st.selectbox("Coluna de ID Transação/Pedido:", cols_available, index=def_trx_idx)
        col_val = st.selectbox("Coluna de Valor Total (R$):", cols_available, index=def_val_idx)

    # Conversão de datas para filtro
    raw_df[col_date] = pd.to_datetime(raw_df[col_date], errors="coerce")
    valid_dates_df = raw_df.dropna(subset=[col_date])

    if valid_dates_df.empty:
        st.error("A coluna de datas selecionada não possui datas válidas.")
        st.stop()

    min_date = valid_dates_df[col_date].min().date()
    max_date = valid_dates_df[col_date].max().date()

    st.markdown("---")
    st.subheader("📅 3. Filtro Temporal")
    selected_date_range = st.date_input(
        "Período de Análise:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Aplicação do filtro temporal
    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        start_d, end_d = selected_date_range
        filtered_raw_df = raw_df[
            (raw_df[col_date].dt.date >= start_d) & (raw_df[col_date].dt.date <= end_d)
        ]
    else:
        filtered_raw_df = raw_df.copy()

    if filtered_raw_df.empty:
        st.warning("Nenhum dado encontrado para o período selecionado.")
        st.stop()


# ==============================================================================
# PROCESSAMENTO DO MOTOR RFM
# ==============================================================================
try:
    with st.spinner("Calculando Recência, Frequência, Valor e Clusters..."):
        rfm_df = calculate_rfm(
            filtered_raw_df,
            customer_col=col_cli,
            date_col=col_date,
            transaction_col=col_trx,
            value_col=col_val,
        )
except Exception as e:
    st.error(f"Erro ao processar métricas RFM: {e}")
    st.stop()

# Filtro de clusters na barra lateral
all_clusters = list(CLUSTER_METADATA.keys())
with st.sidebar:
    st.markdown("---")
    st.subheader("👥 4. Filtro de Segmentos")
    selected_clusters = st.multiselect(
        "Filtrar clusters específicos:",
        options=all_clusters,
        default=all_clusters,
        help="Permite isolar um ou mais grupos de clientes para inspeção e exportação.",
    )

    if not selected_clusters:
        st.warning("Selecione ao menos um segmento para visualizar.")
        st.stop()

# Aplica filtro de clusters
active_rfm_df = rfm_df[rfm_df["Segmento"].isin(selected_clusters)].copy()
cluster_summary = summarize_clusters(active_rfm_df)


# ==============================================================================
# HEADER PRINCIPAL
# ==============================================================================
col_title, col_logo = st.columns([0.88, 0.12])
with col_title:
    st.title("🎯 Cockpit Analítico de Segmentação RFM")
    st.markdown(
        "Diagnóstico estratégico da base de clientes através dos pilares de **Recência**, "
        "**Frequência** e **Valor Monetário**. Identifique receita em risco e direcione planos de ação táticos para CRM e Vendas."
    )
with col_logo:
    st.caption("Status: Online")
    st.caption(f"Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")


# ==============================================================================
# CARDS DE KPIS EXECUTIVOS (C-LEVEL)
# ==============================================================================
total_revenue = float(active_rfm_df["Valor"].sum())
total_clients = int(len(active_rfm_df))
avg_ticket = float(active_rfm_df["Valor"].sum() / active_rfm_df["Frequencia"].sum()) if active_rfm_df["Frequencia"].sum() > 0 else 0.0

# Cálculo da Receita em Risco ('Em Risco' + 'Não Podemos Perder')
risk_segments = ["Em Risco", "Não Podemos Perder"]
risk_df = rfm_df[rfm_df["Segmento"].isin(risk_segments)]
risk_revenue = float(risk_df["Valor"].sum())
risk_clients = int(len(risk_df))
global_revenue = float(rfm_df["Valor"].sum())
risk_share = (risk_revenue / global_revenue * 100) if global_revenue > 0 else 0.0

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Receita Filtrada</div>
            <div class="metric-value">R$ {total_revenue:,.2f}</div>
            <div class="metric-subtext">Volume transacionado no período</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Clientes Únicos</div>
            <div class="metric-value">{total_clients:,}</div>
            <div class="metric-subtext">Base analisada com compras ativas</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Ticket Médio Geral</div>
            <div class="metric-value">R$ {avg_ticket:,.2f}</div>
            <div class="metric-subtext">Gasto médio por pedido</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col4:
    st.markdown(
        f"""
        <div class="metric-card metric-alert">
            <div class="metric-label" style="color:#EF4444;">🚨 Receita em Risco</div>
            <div class="metric-value" style="color:#EF4444;">R$ {risk_revenue:,.2f}</div>
            <div class="metric-subtext"><b>{risk_share:.1f}%</b> da base global ({risk_clients} clientes)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")


# ==============================================================================
# VISUALIZAÇÕES INTERATIVAS (PLOTLY)
# ==============================================================================
st.subheader("📊 Diagnóstico Visual da Base de Clientes")

tab_treemap, tab_scatter, tab_heatmap = st.tabs(
    [
        "🌳 Visão Treemap (Mix & Volume)",
        "🪐 Dispersão Espacial (2D / 3D)",
        "🔥 Matriz de Calor RFM (Concentração)",
    ]
)

# Paleta de cores para os gráficos
color_map = {seg: data["cor"] for seg, data in CLUSTER_METADATA.items()}

# ------------------------------------------------------------------------------
# ABA 1: TREEMAP DE SEGMENTAÇÃO
# ------------------------------------------------------------------------------
with tab_treemap:
    col_t_ctrl, col_t_empty = st.columns([0.4, 0.6])
    with col_t_ctrl:
        treemap_metric = st.radio(
            "Dimensionar blocos por:",
            options=["Receita Total (R$)", "Quantidade de Clientes"],
            horizontal=True,
        )

    val_col = "Receita_Total" if treemap_metric == "Receita_Total (R$)" else "Qtd_Clientes"

    fig_tree = px.treemap(
        cluster_summary,
        path=["Segmento"],
        values=val_col,
        color="Segmento",
        color_discrete_map=color_map,
        custom_data=["Qtd_Clientes", "Perc_Clientes", "Receita_Total", "Perc_Receita", "Ticket_Medio"],
    )

    fig_tree.update_traces(
        textinfo="label+value+percent root",
        hovertemplate=(
            "<b>Segmento: %{label}</b><br><br>"
            "👥 Clientes: %{customdata[0]:,} (%{customdata[1]:.1f}%)<br>"
            "💰 Receita: R$ %{customdata[2]:,.2f} (%{customdata[3]:.1f}%)<br>"
            "🏷️ Ticket Médio: R$ %{customdata[4]:,.2f}<br>"
            "<extra></extra>"
        ),
    )
    fig_tree.update_layout(
        margin=dict(t=10, l=10, r=10, b=10),
        height=480,
    )
    st.plotly_chart(fig_tree, use_container_width=True)


# ------------------------------------------------------------------------------
# ABA 2: GRÁFICO DE DISPERSÃO (2D E 3D)
# ------------------------------------------------------------------------------
with tab_scatter:
    col_sc_mode, col_sc_sample = st.columns([0.4, 0.6])
    with col_sc_mode:
        scatter_dimension = st.radio(
            "Modo de Visualização:",
            options=["Dispersão 2D (Recência vs Frequência)", "Exploração 3D (R x F x M)"],
            horizontal=True,
        )

    # Limita amostra se a base for muito grande para manter fluidez gráfica
    plot_data = active_rfm_df
    if len(plot_data) > 2500:
        plot_data = plot_data.sample(n=2500, random_state=42)
        st.caption("ℹ️ Exibindo amostra representativa de 2.500 clientes para otimizar desempenho interativo.")

    if scatter_dimension == "Dispersão 2D (Recência vs Frequência)":
        fig_scatter = px.scatter(
            plot_data,
            x="Recencia",
            y="Frequencia",
            size="Valor",
            color="Segmento",
            color_discrete_map=color_map,
            hover_name="id_cliente",
            hover_data={
                "Recencia": True,
                "Frequencia": True,
                "Valor": ":,.2f",
                "RFM_Score": True,
                "Segmento": True,
            },
            labels={
                "Recencia": "Recência (Dias sem comprar)",
                "Frequencia": "Frequência (Nº de Pedidos)",
                "Valor": "Valor Total (R$)",
            },
            size_max=35,
            opacity=0.8,
        )
        fig_scatter.update_layout(
            height=500,
            margin=dict(t=20, l=20, r=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    else:
        fig_3d = px.scatter_3d(
            plot_data,
            x="Recencia",
            y="Frequencia",
            z="Valor",
            color="Segmento",
            color_discrete_map=color_map,
            hover_name="id_cliente",
            hover_data={
                "Recencia": True,
                "Frequencia": True,
                "Valor": ":,.2f",
                "RFM_Score": True,
            },
            labels={
                "Recencia": "Recência (Dias)",
                "Frequencia": "Frequência (Qtd)",
                "Valor": "Valor Total (R$)",
            },
            opacity=0.75,
        )
        fig_3d.update_layout(
            height=580,
            margin=dict(t=10, l=10, r=10, b=10),
            scene=dict(
                xaxis_title="Recência (Dias)",
                yaxis_title="Frequência (Compras)",
                zaxis_title="Monetário (R$)",
            ),
        )
        st.plotly_chart(fig_3d, use_container_width=True)


# ------------------------------------------------------------------------------
# ABA 3: MATRIZ DE CALOR RFM (5x5)
# ------------------------------------------------------------------------------
with tab_heatmap:
    st.caption("A matriz 5x5 cruza os scores de Recência (eixo Y) e Frequência (eixo X). Células mais escuras indicam maior densidade de clientes.")

    # Tabela pivô de densidade de clientes por R_Score e F_Score
    heatmap_matrix = pd.crosstab(
        index=active_rfm_df["R_Score"],
        columns=active_rfm_df["F_Score"],
        values=active_rfm_df["Valor"],
        aggfunc="count",
    ).fillna(0).astype(int)

    # Garante estrutura 5x5 mesmo com filtros
    for i in range(1, 6):
        if i not in heatmap_matrix.index:
            heatmap_matrix.loc[i] = 0
        if i not in heatmap_matrix.columns:
            heatmap_matrix[i] = 0
    heatmap_matrix = heatmap_matrix.sort_index(ascending=False).sort_index(axis=1)

    # Receita acumulada por célula para tooltip
    revenue_matrix = pd.crosstab(
        index=active_rfm_df["R_Score"],
        columns=active_rfm_df["F_Score"],
        values=active_rfm_df["Valor"],
        aggfunc="sum",
    ).fillna(0).round(2)
    for i in range(1, 6):
        if i not in revenue_matrix.index:
            revenue_matrix.loc[i] = 0.0
        if i not in revenue_matrix.columns:
            revenue_matrix[i] = 0.0
    revenue_matrix = revenue_matrix.sort_index(ascending=False).sort_index(axis=1)

    # Texto das células anotadas
    annotations_text = [
        [f"{val:,} cli<br>R$ {rev:,.0f}" for val, rev in zip(row_val, row_rev)]
        for row_val, row_rev in zip(heatmap_matrix.values, revenue_matrix.values)
    ]

    fig_heat = go.Figure(
        data=go.Heatmap(
            z=heatmap_matrix.values,
            x=[f"F{i}" for i in heatmap_matrix.columns],
            y=[f"R{i}" for i in heatmap_matrix.index],
            text=annotations_text,
            texttemplate="%{text}",
            textfont={"size": 11},
            colorscale="Blues",
            colorbar=dict(title="Qtd Clientes"),
            hoverongaps=False,
        )
    )

    fig_heat.update_layout(
        title="Concentração da Base: Score de Recência vs Score de Frequência",
        xaxis_title="Score de Frequência (F1 = Menor Frequência ➡️ F5 = Maior Frequência)",
        yaxis_title="Score de Recência (R1 = Mais Antigo ➡️ R5 = Comprou Recentemente)",
        height=480,
        margin=dict(t=40, l=40, r=40, b=40),
    )
    st.plotly_chart(fig_heat, use_container_width=True)

st.write("")


# ==============================================================================
# TABELA OPERACIONAL DE AÇÃO & PLAYBOOK TÁTICO
# ==============================================================================
st.subheader("📋 Tabela Operacional de Ação & Playbook Tático")
st.markdown("Selecione um segmento para consultar a orientação estratégica e baixar a lista de clientes para abordagem imediata.")

col_sel_seg, col_search = st.columns([0.45, 0.55])
with col_sel_seg:
    foco_segmento = st.selectbox(
        "Foco Tático por Segmento:",
        options=["Todos os Segmentos Filtrados"] + [s for s in all_clusters if s in selected_clusters],
        index=0,
    )

with col_search:
    termo_busca = st.text_input(
        "🔍 Buscar cliente específico:",
        placeholder="Digite o ID do cliente...",
    )

# Filtragem dos dados da tabela operacional
tabela_operacional = active_rfm_df.copy()
if foco_segmento != "Todos os Segmentos Filtrados":
    tabela_operacional = tabela_operacional[tabela_operacional["Segmento"] == foco_segmento]

if termo_busca:
    tabela_operacional = tabela_operacional[
        tabela_operacional["id_cliente"].astype(str).str.contains(termo_busca, case=False, na=False)
    ]

# Card com Playbook Tático se um segmento específico for focado
if foco_segmento != "Todos os Segmentos Filtrados":
    meta = CLUSTER_METADATA.get(foco_segmento, {})
    prio = meta.get("prioridade", "Média")
    prio_class = f"badge-{prio.lower().replace(' ', '-')}"

    st.markdown(
        f"""
        <div class="action-card" style="border-left-color: {meta.get('cor', '#3B82F6')};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <h4 style="margin: 0; color: {meta.get('cor', '#3B82F6')}; font-weight: 700;">
                    🎯 Playbook Comercial: {foco_segmento}
                </h4>
                <span class="badge {prio_class}">Prioridade: {prio}</span>
            </div>
            <p style="margin-bottom: 8px;"><b>Perfil:</b> {meta.get('descricao', '')}</p>
            <p style="margin-bottom: 8px;"><b>Objetivo Estratégico:</b> {meta.get('objetivo', '')}</p>
            <p style="margin-bottom: 8px; white-space: pre-line;"><b>Ações Recomendadas:</b><br>{meta.get('plano_de_acao', '')}</p>
            <p style="margin-bottom: 0;"><b>Canais Sugeridos:</b> <code>{meta.get('canais_recomendados', '')}</code></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Resumo rápido da lista selecionada
col_res1, col_res2, col_res3, col_exp = st.columns([0.2, 0.2, 0.2, 0.4])
with col_res1:
    st.metric("Clientes Listados", f"{len(tabela_operacional):,}")
with col_res2:
    st.metric("Receita Deste Grupo", f"R$ {tabela_operacional['Valor'].sum():,.2f}")
with col_res3:
    media_ticket_grupo = (
        tabela_operacional["Valor"].sum() / tabela_operacional["Frequencia"].sum()
        if tabela_operacional["Frequencia"].sum() > 0
        else 0
    )
    st.metric("Ticket Médio Grupo", f"R$ {media_ticket_grupo:,.2f}")

# Botão de exportação em CSV formatado para CRM
with col_exp:
    st.write("")
    csv_buffer = io.StringIO()
    # UTF-8 com BOM para garantir abertura nativa e sem distorções no Excel em português
    tabela_operacional.to_csv(csv_buffer, index=False, sep=";", encoding="utf-8-sig")
    csv_bytes = csv_buffer.getvalue().encode("utf-8-sig")

    nome_arquivo = (
        f"rfm_{foco_segmento.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"
        if foco_segmento != "Todos os Segmentos Filtrados"
        else f"rfm_base_completa_{datetime.now().strftime('%Y%m%d')}.csv"
    )

    st.download_button(
        label="📥 Exportar Lista para CRM / Vendas (CSV)",
        data=csv_bytes,
        file_name=nome_arquivo,
        mime="text/csv",
        use_container_width=True,
    )

# Exibição da tabela de dados formatada
colunas_exibicao = [
    "id_cliente",
    "Segmento",
    "Prioridade_Acao",
    "Recencia",
    "Frequencia",
    "Valor",
    "Ticket_Medio",
    "R_Score",
    "F_Score",
    "M_Score",
    "RFM_Score",
]

colunas_renomeadas = {
    "id_cliente": "ID Cliente",
    "Segmento": "Segmento RFM",
    "Prioridade_Acao": "Prioridade",
    "Recencia": "Recência (Dias)",
    "Frequencia": "Frequência (Compras)",
    "Valor": "Valor Total (R$)",
    "Ticket_Medio": "Ticket Médio (R$)",
    "R_Score": "R",
    "F_Score": "F",
    "M_Score": "M",
    "RFM_Score": "Score RFM",
}

tabela_view = tabela_operacional[colunas_exibicao].rename(columns=colunas_renomeadas)

st.dataframe(
    tabela_view.sort_values(by="Valor Total (R$)", ascending=False),
    use_container_width=True,
    hide_index=True,
    height=400,
)

# ==============================================================================
# RODAPÉ INFORMATIVO
# ==============================================================================
st.markdown("---")
st.caption(
    "💡 **Metodologia RFM**: Os scores R, F e M são calculados via quantis (quintis de 1 a 5) com resolução determinística de empates. "
    "Aplicação desenvolvida para diagnóstico de base e suporte a decisões de Retenção, Fidelização e Vendas."
)
