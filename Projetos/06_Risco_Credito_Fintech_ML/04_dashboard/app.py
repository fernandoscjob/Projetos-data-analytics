import streamlit as st
import pandas as pd
import joblib
import os
import plotly.express as px
from google.cloud import bigquery
from dotenv import load_dotenv

# Carrega variáveis
load_dotenv()

st.set_page_config(page_title="Fintech Analytics & Risk", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

# ==========================================
# CUSTOM CSS PARA UX DESIGN
# ==========================================
st.markdown("""
    <style>
    /* Suavizando as cores de fundo dos blocos de métricas */
    div[data-testid="metric-container"] {
        background-color: #1e1e2e;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #2e2e42;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Melhorando a tipografia e espaçamento dos headers */
    h1, h2, h3 {
        color: #f8f9fa !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 5px 5px 0 0;
        font-size: 18px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. FUNÇÕES DE CARREGAMENTO (CACHED)
# ==========================================
@st.cache_data(show_spinner=False)
def carregar_dados_dashboard():
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        return pd.DataFrame()
    bq_client = bigquery.Client(project=project_id)
    query = f"SELECT * FROM `{project_id}.analytics_dev.dim_clientes_credito` LIMIT 10000"
    df = bq_client.query(query).to_dataframe()
    df['Status'] = df['TARGET'].apply(lambda x: 'Inadimplente' if x == 1 else 'Bom Pagador')
    df['Idade'] = (df['DAYS_BIRTH'].abs() / 365).astype(int)
    # Ajuste de categoria de gênero para ficar amigável
    df['CODE_GENDER'] = df['CODE_GENDER'].replace({'M': 'Masculino', 'F': 'Feminino'})
    return df

@st.cache_resource
def carregar_modelo():
    caminho = os.path.join(os.path.dirname(__file__), "..", "03_machine_learning", "modelo_risco_credito.pkl")
    return joblib.load(caminho)

# ==========================================
# SIDEBAR (SOBRE O PROJETO)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3004/3004122.png", width=100)
    st.title("Sobre o Projeto")
    st.info("""
    **Arquitetura End-to-End**
    - **Banco:** Supabase (PostgreSQL)
    - **Data Warehouse:** BigQuery
    - **Transformação:** dbt
    - **Machine Learning:** XGBoost
    """)
    st.markdown("---")
    st.markdown("Desenvolvido como projeto de portfólio de Engenharia e Ciência de Dados.")

# ==========================================
# INTERFACE PRINCIPAL
# ==========================================
st.title("🏦 Fintech Analytics & Risk Engine")
st.markdown("Bem-vindo à plataforma central de decisão de crédito. Navegue pelas abas abaixo.")

aba1, aba2 = st.tabs(["📊 Visão Executiva (BI)", "🤖 Motor de Decisão (AI)"])

with st.spinner("Conectando ao Data Warehouse..."):
    df_dash = carregar_dados_dashboard()

# ==========================================
# ABA 1: DASHBOARD EXECUTIVO
# ==========================================
with aba1:
    if df_dash.empty:
        st.error("Erro ao carregar dados do BigQuery.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        # KPIs Superiores
        col1, col2, col3, col4 = st.columns(4)
        total_clientes = len(df_dash)
        total_credito = df_dash['AMT_CREDIT'].sum()
        taxa_inadimplencia = (df_dash[df_dash['TARGET'] == 1].shape[0] / total_clientes) * 100
        idade_media = df_dash['Idade'].mean()

        col1.metric("Total de Contratos", f"{total_clientes:,}", help="Amostra extraída do BigQuery")
        col2.metric("Crédito Concedido", f"US$ {total_credito/1e6:,.1f} Milhões")
        col3.metric("Taxa de Inadimplência", f"{taxa_inadimplencia:.1f}%", "-0.2%", help="Percentual de clientes que entraram em default")
        col4.metric("Idade Média", f"{idade_media:.0f} anos")
        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        
        # Primeira Linha de Gráficos (Design Clean do Plotly)
        row1_col1, row1_col2 = st.columns([1, 2]) # A coluna da direita é 2x maior
        
        with row1_col1:
            st.markdown("#### Proporção de Risco")
            fig_pizza = px.pie(
                df_dash, 
                names='Status', 
                color='Status',
                color_discrete_map={'Bom Pagador': '#2ab7ca', 'Inadimplente': '#fe4a90'},
                hole=0.6 # Furo maior para design mais elegante (Donut)
            )
            fig_pizza.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
            fig_pizza.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pizza, use_container_width=True)
            
        with row1_col2:
            st.markdown("#### Crédito vs. Renda Anual (Detalhamento)")
            df_filtrado = df_dash[df_dash['AMT_INCOME_TOTAL'] < 400000] # Limpando outliers
            fig_scatter = px.scatter(
                df_filtrado, 
                x="AMT_INCOME_TOTAL", 
                y="AMT_CREDIT", 
                color="Status",
                color_discrete_map={'Bom Pagador': '#2ab7ca', 'Inadimplente': '#fe4a90'},
                opacity=0.7,
                hover_data=['Idade']
            )
            # Remove as linhas de grade para um visual mais limpo
            fig_scatter.update_xaxes(title="Renda Anual (US$)", showgrid=False, zeroline=False)
            fig_scatter.update_yaxes(title="Valor do Crédito Cedido (US$)", showgrid=False)
            fig_scatter.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_scatter, use_container_width=True)

        # Segunda Linha
        st.markdown("#### Perfil de Inadimplência por Contrato")
        df_agrupado = df_dash[df_dash['TARGET'] == 1].groupby(['NAME_CONTRACT_TYPE', 'CODE_GENDER']).size().reset_index(name='Casos Inadimplentes')
        fig_bar = px.bar(
            df_agrupado, 
            x='NAME_CONTRACT_TYPE', 
            y='Casos Inadimplentes', 
            color='CODE_GENDER',
            barmode='group',
            color_discrete_sequence=['#ffca28', '#ab47bc']
        )
        fig_bar.update_xaxes(title="Tipo de Contrato")
        fig_bar.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)

# ==========================================
# ABA 2: MOTOR PREDITIVO (AI)
# ==========================================
with aba2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Calculadora de Score de Crédito")
    st.markdown("Nossa IA processa as mais de 120 variáveis comportamentais do cliente no banco de dados e determina a probabilidade estatística de calote (Default).")
    
    if not df_dash.empty:
        # Layout em container para dar destaque
        with st.container(border=True):
            clientes_dropdown = df_dash.head(200)
            cliente_id = st.selectbox("🔍 Pesquisar ID do Cliente (SK_ID_CURR):", clientes_dropdown['SK_ID_CURR'])

            dados_cliente = df_dash[df_dash['SK_ID_CURR'] == cliente_id].iloc[0]
            
            # Sub-Métricas do Cliente
            st.markdown("##### Dados Básicos")
            c1, c2, c3, c4 = st.columns(4)
            c1.write(f"**Gênero:** {dados_cliente['CODE_GENDER']}")
            c2.write(f"**Idade:** {dados_cliente['Idade']} anos")
            c3.write(f"**Renda Anual:** US$ {dados_cliente['AMT_INCOME_TOTAL']:,.0f}")
            c4.write(f"**Crédito Solicitado:** US$ {dados_cliente['AMT_CREDIT']:,.0f}")
            
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🧠 Executar Análise de Risco", type="primary", use_container_width=True):
                with st.spinner("Algoritmo XGBoost analisando dezenas de árvores de decisão..."):
                    colunas_extras = ['Status', 'Idade']
                    X_cliente = pd.DataFrame([dados_cliente]).drop(columns=['TARGET', 'SK_ID_CURR'] + colunas_extras)
                    
                    modelo = carregar_modelo()
                    probabilidade = float(modelo.predict_proba(X_cliente)[0][1])
                    porcentagem = probabilidade * 100
                    
                st.markdown("---")
                st.markdown("### 🚦 Decisão do Algoritmo:")
                
                # Caixas de destaque baseadas no risco
                if porcentagem > 50:
                    st.error(f"**Risco Crítico:** {porcentagem:.1f}% de chance de inadimplência.")
                    st.progress(probabilidade)
                    st.markdown("> **RECOMENDAÇÃO DE NEGÓCIO:** Operação negada automaticamente. Solicitar revisão e fiador caso o cliente faça contestação.")
                elif porcentagem > 30:
                    st.warning(f"**Risco Moderado/Atenção:** {porcentagem:.1f}% de chance de inadimplência.")
                    st.progress(probabilidade)
                    st.markdown("> **RECOMENDAÇÃO DE NEGÓCIO:** Suspender aprovação automática. Encaminhar para a esteira de revisão humana e solicitar comprovante de renda atualizado.")
                else:
                    st.success(f"**Risco Baixo:** Apenas {porcentagem:.1f}% de chance de inadimplência.")
                    st.progress(probabilidade)
                    st.balloons()
                    st.markdown("> **RECOMENDAÇÃO DE NEGÓCIO:** Crédito aprovado e liberado automaticamente na conta!")

    with st.expander("Como funciona nosso Motor Preditivo?"):
        st.write("""
        Nosso modelo é baseado no algoritmo **XGBoost (Extreme Gradient Boosting)**. 
        Ele foi treinado em uma base desbalanceada utilizando técnicas de peso na classe minoritária (`scale_pos_weight`). 
        Isso força a IA a penalizar mais os erros em maus pagadores, tornando o modelo mais conservador e protegendo o caixa da instituição financeira.
        """)

