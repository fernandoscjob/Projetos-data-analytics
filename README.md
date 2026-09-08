# 📊 Portfólio Profissional | Analista de Dados & Especialista em BI

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![Tema](https://img.shields.io/badge/Tema-Dark_Modern_(Linear/Vercel)-090a0f?style=for-the-badge)
![Tech](https://img.shields.io/badge/Stack-HTML5_•_TailwindCSS_•_Chart.js_•_Vanilla_JS-sky?style=for-the-badge)

Portfólio técnico de **Fernando da Silva Cavalcante** — Analista de Dados | Especialista em BI, com foco em tomada de decisão executiva, redução de custos operacionais, modelagem dimensional e governança analítica.

---

## 🌟 Destaques do Projeto

- **Design System Dark Modern**: Estética refinada inspirada na *Linear* e *Vercel*, com paleta grafite `#090a0f`, gradientes radiais, efeito *glassmorphism* e acabamento visual de alto padrão.
- **Identidade Pessoal & Foto de Perfil**: Foto profissional integrada no Header, Hero Section de duas colunas com tags flutuantes de impacto (`-40% Custos Frete`, `99.8% SLA Dados`) e seção de contato.
- **Barra de Métricas de Impacto (Quick Wins)**: Contadores animados via `IntersectionObserver` apresentando números de ROI, volume e automação.
- **Pilares de Soluções & Geração de Valor (#solucoes)**: Grid consultivo de 4 frentes estratégicas (Auditoria & Otimização de Custos, Camada Semântica & SSOT, BI & Cockpits C-Level e Pipelines & Alertas Proativos).
- **Stack Técnica Categorizada**: Badges interativos distribuídos em *Modelagem & Engenharia* (SQL Avançado, Kimball, Star Schema, SSOT, dbt), *BI & Camada Executiva* (Looker LookML, Power BI, DAX Avançado, Cockpits C-Level), *Automação & Pipelines* (Python, n8n, Alertas Proativos, Airflow) e *Negócio & Governança* (Auditoria Contratual, Cohort Analytics, BPMN Bizagi).
- **5 Cases de Sucesso com Modal Aprofundado**:
  1. **Auditoria Contratual de Fretes & Otimização de Custos** (SQL + Looker + Python).
  2. **Modelagem de Cohort, Retenção & Prevenção de Churn** (SQL Window Functions + dbt).
  3. **Camada Semântica & Cockpit Executivo de Planejamento** (Power BI + dbt + Kimball).
  4. **Orquestração de Pipelines e Alertas Proativos** (n8n + Python + Webhooks).
  5. **Cockpit Analítico de Segmentação RFM & Prevenção de Churn** (Python + Streamlit + Plotly + Quantis).
  *Cada modal contém o desafio de negócio, arquitetura técnica, queries SQL/código Python e resultados de ROI mensuráveis.*
- **Cockpit Analítico Interativo (Chart.js, Cohort Heatmap & Cockpit RFM)**:
  - *Visão 1*: Custo Real vs Meta (Linha comparativa de inflexão).
  - *Visão 2*: Volume Operacional & Acurácia de SLA (Barras e Eixo Secundário).
  - *Visão 3*: **Matriz Heatmap de Cohort & Churn** com alternância em tempo real entre *Taxa de Retenção (%)* e *Taxa de Churn (%)*.
  - *Visão 4*: **Cockpit RFM & CRM** com Matriz 5x5 interativa, cards de receita em risco (R$ 485k) e playbooks comerciais dinâmicos para 11 clusters.
- **Trajetória Profissional & Formação Acadêmica**: Timeline corporativa estruturada com experiências como *Analista de Dados / Consultor de BI* e atuação na MEDGRUPO (Looker Studio, SQL, automações n8n), além de formação em Análise e Desenvolvimento de Sistemas.
- **Formulário de Contato Integrado**: Pronto para o **Formspree** via envio assíncrono (AJAX/Fetch) com feedback via componente *Toast* sem recarregar a página.
- **Links Reais & Download de CV**: Conexão direta com WhatsApp, LinkedIn, GitHub e download nativo do arquivo `curriculo-fernando.pdf`.

---

## 📁 Estrutura de Arquivos Isolada

O repositório é organizado de forma modular e isolada, separando a camada do **Site de Portfólio** dos **5 Projetos de Dados**:

```
Portifólio em Dados/
│
├── 🌐 Site/                                 # ARQUIVOS DO SITE DE PORTFÓLIO (FRONTEND)
│   ├── index.html                          # Aplicação web completa do portfólio
│   ├── dashboard-rfm.html                  # Cockpit Analítico RFM Standalone (Plotly.js)
│   ├── dashboard-fretes.html               # Cockpit de Auditoria de Fretes Standalone (Plotly.js)
│   ├── style.css                           # Design tokens, glassmorphism e animações
│   ├── main.js                             # Lógica interativa, Chart.js, Cohort e AJAX
│   ├── profile.jpg                         # Foto de perfil profissional em alta resolução
│   ├── curriculo-fernando.pdf              # Arquivo de currículo para download direto
│   └── video_dashboard.mp4                 # Vídeo demonstrativo dos dashboards
│
├── 📊 Projetos/                             # PROJETOS DE ENGENHARIA, ANALYTICS E BI
│   │
│   ├── 01_Cockpit_RFM_Analytics/           # Projeto 01: Segmentação RFM & Prevenção de Churn
│   │   ├── app.py                          # Aplicação Web analítica executiva em Streamlit
│   │   ├── rfm_engine.py                   # Motor de cálculo RFM por quantis e 11 clusters
│   │   ├── requirements.txt                # Dependências (streamlit, pandas, numpy, plotly)
│   │   └── README.md                       # Documentação técnica detalhada do projeto
│   │
│   ├── 02_Auditoria_Fretes_Logistica/      # Projeto 02: Auditoria Contratual de Fretes & Glosas
│   │   ├── app.py                          # Aplicação Web executiva em Streamlit & Plotly
│   │   ├── auditoria_fretes.py             # Script de conciliação de faturas vs contrato
│   │   ├── queries_auditoria.sql           # Pipeline SQL avançado (CTEs e Window Functions)
│   │   ├── requirements.txt                # Dependências (streamlit, pandas, numpy, plotly)
│   │   └── README.md                       # Documentação com regras de cubagem e ROI
│   │
│   ├── 03_Cohort_Retencao_Churn/           # Projeto 03: Modelagem de Cohort & Churn
│   │   ├── cohort_model.py                 # Modelo Python de safras e curvas de retenção
│   │   ├── cohort_pipeline.sql             # Pipeline dbt / BigQuery SQL de sobrevivência
│   │   ├── requirements.txt                # Dependências (pandas, numpy)
│   │   └── README.md                       # Documentação de Early Churn e retenção
│   │
│   ├── 04_Camada_Semantica_Cockpit_BI/     # Projeto 04: Camada Semântica & Modelagem Kimball
│   │   ├── dbt_models/                     # Modelos dbt (dim_clientes, dim_produtos, dim_calendario, fct_vendas, schema.yml)
│   │   ├── medidas_dax_corporativas.dax    # Catálogo com 14 métricas corporativas DAX
│   │   └── README.md                       # Documentação de SSOT e governança dimensional
│   │
│   └── 05_Orquestracao_Alertas_Anomalias/  # Projeto 05: Orquestração de Pipelines e Alertas
│       ├── anomaly_detector.py             # Motor estatístico de cálculo de Z-Score (> 2.5)
│       ├── n8n_workflow_alertas.json       # Workflow n8n exportado com webhooks
│       ├── requirements.txt                # Dependências (pandas, numpy, requests)
│       └── README.md                       # Guia de integração n8n e webhooks Slack
│
├── index.html                              # Redirecionamento instantâneo para Site/index.html (compatibilidade GitHub Pages)
├── .gitignore                              # Ignora ambientes virtuais (.venv) e caches
└── README.md                               # Documentação geral do repositório
```

---

## 🚀 Como Executar os Projetos Localmente

### 🌐 Abrir o Portfólio Web (Pasta `Site/`)
- **Direto pelo Navegador**: Dê dois cliques em [`Site/index.html`](Site/index.html) ou no [`index.html`](index.html) da raiz (que redireciona automaticamente para o site).
- **Via VS Code Live Server**: Abra a pasta `Site/` ou a raiz no VS Code e inicie com o Live Server.
- **Via Servidor Local Python**:
  ```bash
  python -m http.server 3000
  ```
  Acesse no navegador: `http://localhost:3000/Site/index.html`.

### 📊 Executar os Projetos de Dados em Python

1. **Projeto 01 - Cockpit RFM (Streamlit):**
   ```bash
   streamlit run Projetos/01_Cockpit_RFM_Analytics/app.py
   ```
   *Acesse a aplicação no navegador em `http://localhost:8501`.*

2. **Projeto 02 - Auditoria de Fretes & Glosas (Streamlit / Python / SQL):**
   ```bash
   streamlit run Projetos/02_Auditoria_Fretes_Logistica/app.py
   ```
   *Ou execução direta via CLI:*
   ```bash
   python Projetos/02_Auditoria_Fretes_Logistica/auditoria_fretes.py
   ```

3. **Projeto 03 - Modelagem de Cohort & Retenção (Python/dbt):**
   ```bash
   python Projetos/03_Cohort_Retencao_Churn/cohort_model.py
   ```

4. **Projeto 04 - Camada Semântica & Modelagem Dimensional (dbt/DAX):**
   - Inspecione os modelos em [`Projetos/04_Camada_Semantica_Cockpit_BI/dbt_models/`](Projetos/04_Camada_Semantica_Cockpit_BI/dbt_models/) e a biblioteca de medidas em [`medidas_dax_corporativas.dax`](Projetos/04_Camada_Semantica_Cockpit_BI/medidas_dax_corporativas.dax).

5. **Projeto 05 - Detector de Anomalias & Alertas (n8n/Python):**
   ```bash
   python Projetos/05_Orquestracao_Alertas_Anomalias/anomaly_detector.py
   ```

### ⚡ Dashboard RFM Standalone Direto no Navegador (Sem Python)
Dê dois cliques no arquivo [`Site/dashboard-rfm.html`](Site/dashboard-rfm.html). Ele funciona diretamente no navegador sem exigir servidor Python em execução.

---

## ✉️ Configuração do Formulário de Contato (Formspree)

O formulário já está configurado e integrado com o endpoint:
```html
<form id="contactForm" action="https://formspree.io/f/xeaqrrnr" method="POST" ...>
```
O envio ocorre de forma assíncrona (AJAX/Fetch), apresentando um spinner de carregamento no botão, limpando os campos e disparando o componente Toast com mensagem de confirmação de envio sem recarregar a página. Caso deseje alterar para outro endpoint no futuro, basta atualizar o atributo `action` no arquivo `index.html`.

---

## 📄 Atualização do Currículo (PDF)

Para atualizar o currículo baixado pelos visitantes:
1. Exporte seu currículo atualizado em formato PDF.
2. Renomeie o arquivo para:
   ```
   curriculo-fernando.pdf
   ```
3. Substitua o arquivo existente na raiz do projeto mantendo o mesmo nome. O botão **"Baixar CV Completo"** fará o download da versão mais recente automaticamente.

---

## 🌐 Instruções de Publicação (Deploy)

### Deploy no GitHub Pages (Gratuito)
1. Crie um repositório no seu GitHub com o nome `portfolio` ou `portfolio-data-analytics`.
2. No terminal da pasta, inicialize o git e suba os arquivos:
   ```bash
   git init
   git add .
   git commit -m "feat: portfolio pronto para producao"
   git branch -M main
   git remote add origin https://github.com/fernandoscjob/Projetos-data-analytics.git # ou seu repositorio especifico
   git push -u origin main
   ```
3. No GitHub, acesse **Settings** > **Pages**.
4. Em **Source**, selecione `Deploy from a branch`, escolha a branch `main` e a pasta `/ (root)`.
5. Salve. Seu portfólio estará online em `https://fernandoscjob.github.io/...` com HTTPS ativo.

### Deploy na Vercel (Recomendado para SPA/Estático)
1. Acesse [vercel.com](https://vercel.com) e conecte com seu GitHub.
2. Clique em **"Add New Project"** e selecione o repositório do portfólio.
3. Clique em **Deploy**. O site será publicado instantaneamente com CDN global de altíssima velocidade.

---

## 📬 Contatos & Redes Profissionais

- **LinkedIn**: [fernando-cavalcante-a478191b1](https://www.linkedin.com/in/fernando-cavalcante-a478191b1/)
- **GitHub**: [fernandoscjob](https://github.com/fernandoscjob/Projetos-data-analytics)
- **WhatsApp**: [+55 (21) 96924-1760](https://wa.me/5521969241760?text=Ol%C3%A1%20Fernando,%20vi%20seu%20portf%C3%B3lio.)
- **E-mail**: [fernandoc.job@gmail.com](mailto:fernandoc.job@gmail.com)

---

*Desenvolvido com foco em alta performance, usabilidade moderna e impacto direto em negócios.*
