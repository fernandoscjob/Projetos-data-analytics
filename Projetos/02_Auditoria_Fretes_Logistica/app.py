"""
Aplicação Streamlit: Cockpit de Auditoria Contratual de Fretes & Glosas
=======================================================================
Interface executiva para auditoria automática de CT-es, detecção de
cobranças indevidas de frete e geração de cartas de contestação.
"""

from datetime import datetime
import io
import os
import sys

# Garante import do módulo mesmo executado da raiz
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from auditoria_fretes import (
    gerar_base_sintetica_ctes,
    recalcular_auditoria_dinamica,
    executar_auditoria,
)

# ==============================================================================
# CONFIGURAÇÃO GERAL
# ==============================================================================
st.set_page_config(
    page_title="Cockpit de Auditoria de Fretes",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ESTILIZAÇÃO CSS CUSTOMIZADA (DARK MODERN / LINEAR STYLE)
# ==============================================================================
st.markdown(
    """
    <style>
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 1rem;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }
    .metric-alert {
        border-left: 4px solid #f43f5e !important;
        background: linear-gradient(135deg, rgba(244, 63, 94, 0.08) 0%, rgba(244, 63, 94, 0.02) 100%);
    }
    .metric-success {
        border-left: 4px solid #10b981 !important;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(16, 185, 129, 0.02) 100%);
    }
    .metric-title {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        font-family: monospace;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 0.75rem;
        margin-top: 0.35rem;
        color: #64748b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# BARRA LATERAL (CONTROLES E PARÂMETROS)
# ==============================================================================
st.sidebar.markdown("### ⚙️ Parâmetros de Auditoria")

modo_dados = st.sidebar.radio(
    "Fonte de Dados:",
    ["Base Calibrada do Caso (800 CT-es - 14 Transportadoras)", "Upload de Arquivo (CSV/Excel)"],
    index=0,
)

df_raw = None

if modo_dados == "Upload de Arquivo (CSV/Excel)":
    uploaded_file = st.sidebar.file_uploader(
        "Carregar CT-es:", type=["csv", "xlsx", "xls"]
    )
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_file)
            else:
                df_raw = pd.read_excel(uploaded_file)
            st.sidebar.success(f"{len(df_raw)} registros carregados!")
        except Exception as e:
            st.sidebar.error(f"Erro ao ler arquivo: {e}")
    else:
        st.sidebar.info("Carregue uma planilha ou utilize a base simulada.")
        df_raw = gerar_base_sintetica_ctes(800)
else:
    tamanho_amostra = st.sidebar.slider("Amostra de CT-es:", 100, 2000, 800, step=50)
    df_raw = gerar_base_sintetica_ctes(tamanho_amostra)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Regras Contratuais")

fator_cubagem = st.sidebar.slider(
    "Fator de Cubagem (kg/m³):", min_value=200.0, max_value=400.0, value=300.0, step=10.0
)

tolerancia_glosa = st.sidebar.slider(
    "Tolerância de Glosa (R$):", min_value=0.0, max_value=50.0, value=10.0, step=2.0
)

aliquota_gris_pct = st.sidebar.slider(
    "Alíquota GRIS / Seguro (%):", min_value=0.1, max_value=1.0, value=0.3, step=0.05
)

# Recalcular dados com parâmetros dinâmicos
df_auditado = recalcular_auditoria_dinamica(
    df_raw,
    fator_cubagem=fator_cubagem,
    tolerancia_glosa=tolerancia_glosa,
    aliquota_gris=aliquota_gris_pct / 100.0,
)

# Filtros da Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filtros Analíticos")

transportadoras_disponiveis = sorted(df_auditado["transportadora"].unique().tolist())
transp_selecionadas = st.sidebar.multiselect(
    "Transportadoras:", transportadoras_disponiveis, default=transportadoras_disponiveis
)

status_disponiveis = sorted(df_auditado["status_auditoria"].unique().tolist())
status_selecionados = st.sidebar.multiselect(
    "Status de Auditoria:", status_disponiveis, default=status_disponiveis
)

# Aplica filtros
df_filtrado = df_auditado[
    (df_auditado["transportadora"].isin(transp_selecionadas))
    & (df_auditado["status_auditoria"].isin(status_selecionados))
]

# ==============================================================================
# CABEÇALHO DO DASHBOARD
# ==============================================================================
st.title("🚚 Cockpit de Auditoria Contratual de Fretes")
st.caption(
    "Plataforma analítica para conciliação automatizada de fretes, detecção de divergências de pesagem/cubagem e recuperação de faturamento indevido (glosas)."
)

# ==============================================================================
# KPIS EXECUTIVOS
# ==============================================================================
kpis = executar_auditoria(df_filtrado)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Faturado (Transportadoras)</div>
            <div class="metric-value">R$ {kpis['total_faturado']:,.2f}</div>
            <div class="metric-sub">{kpis['total_ctes']} CT-es analisados</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="metric-card metric-success">
            <div class="metric-title">Valor Devido (Contratual)</div>
            <div class="metric-value text-emerald-400">R$ {kpis['total_devido']:,.2f}</div>
            <div class="metric-sub">Tarifas contratuais recalculadas</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="metric-card metric-alert">
            <div class="metric-title">🚨 Glosas a Recuperar</div>
            <div class="metric-value text-rose-400">R$ {kpis['total_glosa_recuperavel']:,.2f}</div>
            <div class="metric-sub">{kpis['pct_glosa']}% de sobretaxa indevida</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    pct_glosados = (
        (kpis["ctes_glosados"] / kpis["total_ctes"]) * 100.0
        if kpis["total_ctes"] > 0
        else 0
    )
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">CT-es com Divergência</div>
            <div class="metric-value">{kpis['ctes_glosados']}</div>
            <div class="metric-sub">{pct_glosados:.1f}% de assertividade na rejeição</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==============================================================================
# GRÁFICOS ANALÍTICOS (PLOTLY)
# ==============================================================================
st.markdown("### 📊 Diagnóstico Visual de Divergências")

col_left, col_right = st.columns(2)

with col_left:
    # 1. Comparativo Faturado vs Devido por Transportadora
    resumo_transp = kpis["resumo_transportadora"]
    fig_bar = go.Figure()
    fig_bar.add_trace(
        go.Bar(
            name="Faturado",
            x=resumo_transp["transportadora"],
            y=resumo_transp["total_faturado"],
            marker_color="#38bdf8",
        )
    )
    fig_bar.add_trace(
        go.Bar(
            name="Devido Contratual",
            x=resumo_transp["transportadora"],
            y=resumo_transp["total_devido"],
            marker_color="#10b981",
        )
    )
    fig_bar.add_trace(
        go.Bar(
            name="Glosa / Cobrança Indevida",
            x=resumo_transp["transportadora"],
            y=resumo_transp["total_glosa"],
            marker_color="#f43f5e",
        )
    )
    fig_bar.update_layout(
        title="Faturado vs Devido vs Glosas por Transportadora",
        barmode="group",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    # 2. Distribuição dos Motivos de Glosa (Donut Chart)
    glosas_df = df_filtrado[df_filtrado["divergencia"] > 0]
    if not glosas_df.empty:
        motivos_count = (
            glosas_df.groupby("motivo_auditoria")["divergencia"].sum().reset_index()
        )
        fig_donut = px.pie(
            motivos_count,
            values="divergencia",
            names="motivo_auditoria",
            title="Distribuição Financeira dos Motivos de Glosa (R$)",
            hole=0.55,
            color_discrete_sequence=["#f43f5e", "#fbbf24", "#a855f7", "#38bdf8"],
        )
        fig_donut.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("Nenhuma glosa detectada para os filtros selecionados.")

# 3. Dispersão de Pesagem: Peso Real vs Peso Cubado
st.markdown("### ⚖️ Auditoria de Cubagem Volumétrica (Peso Real vs Peso Cubado)")
st.caption(
    "Pontos acima da linha tracejada indicam fretes tarifados pela cubagem volumétrica em detrimento do peso físico real."
)

fig_scatter = px.scatter(
    df_filtrado,
    x="peso_real_kg",
    y="peso_cubado_kg",
    color="status_auditoria",
    size="divergencia",
    hover_data=["numero_cte", "transportadora", "valor_faturado", "valor_devido"],
    color_discrete_map={
        "REJEITADO / GLOSA": "#f43f5e",
        "APROVADO": "#10b981",
        "REVISÃO MANUAL": "#fbbf24",
    },
    title="Dispersão de Cubagem e Detecção de Superestimativas",
)

# Adiciona linha de paridade (peso real = peso cubado)
max_val = max(
    df_filtrado["peso_real_kg"].max(), df_filtrado["peso_cubado_kg"].max()
)
fig_scatter.add_trace(
    go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode="lines",
        name="Paridade Real/Cubado",
        line=dict(color="#64748b", dash="dash"),
    )
)

fig_scatter.update_layout(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=20, t=50, b=20),
)
st.plotly_chart(fig_scatter, use_container_width=True)

# ==============================================================================
# TABELA OPERACIONAL & EXPORTAÇÃO DE GLOSAS
# ==============================================================================
st.markdown("### 📋 Listagem de CT-es & Carta de Contestação")

col_search, col_action = st.columns([3, 1])

with col_search:
    busca_cte = st.text_input("Buscar por CT-e ou Cidade de Destino:", "")

if busca_cte:
    df_tabela = df_filtrado[
        df_filtrado["numero_cte"].str.contains(busca_cte, case=False)
        | df_filtrado["cidade_destino"].str.contains(busca_cte, case=False)
    ]
else:
    df_tabela = df_filtrado

colunas_view = [
    "numero_cte",
    "transportadora",
    "cidade_destino",
    "data_emissao",
    "peso_real_kg",
    "peso_cubado_kg",
    "valor_faturado",
    "valor_devido",
    "divergencia",
    "status_auditoria",
    "motivo_auditoria",
]

st.dataframe(
    df_tabela[colunas_view].sort_values(by="divergencia", ascending=False),
    use_container_width=True,
    height=320,
)

# Exportação CSV com UTF-8 BOM para Excel
csv_buffer = io.BytesIO()
df_glosas_export = df_filtrado[df_filtrado["divergencia"] > 0].copy()
csv_data = df_glosas_export.to_csv(index=False, sep=";", encoding="utf-8-sig")

with col_action:
    st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Exportar Carta de Glosas (CSV)",
        data=csv_data.encode("utf-8-sig"),
        file_name=f"carta_contestacao_glosas_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True,
    )
