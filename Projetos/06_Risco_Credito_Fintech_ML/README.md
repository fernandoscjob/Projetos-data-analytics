# 🏦 Motor Preditivo de Risco de Crédito: Prevenção de Calotes com IA e Engenharia de Dados

### 🚀 1. TLDR (Too Long; Didn't Read) - Resumo Executivo
*Plataforma End-to-End de Analytics e Machine Learning para tomada de decisão em concessão de crédito.*
- **Objetivo do Projeto:** Desenvolver um motor automatizado de classificação de risco de crédito para identificar clientes propensos à inadimplência (default), reduzindo as perdas financeiras (NPL - Non-Performing Loans).
- **Métricas Principais de Performance:** O modelo atingiu **0.76 de ROC-AUC** no ambiente de validação e alavancou o *Recall* da classe minoritária (Maus Pagadores) em mais de **50x**, bloqueando dezenas de calotes sem intervenção humana.
- **Retorno Financeiro / Eficiência Gerada:** Mitigação projetada de perdas na casa dos milhões de dólares ao restringir 58% dos calotes antes da aprovação do crédito, compensando o leve aumento de falsos positivos na base de clientes.
- **Tempo de Execução / Resposta:** Decisão de aprovação de crédito reduzida de análise manual humana (horas) para processamento em tempo real (milissegundos) no Dashboard Executivo e Operacional.

---

### 💼 2. O Problema de Negócio (Business Understanding)
- **Cenário Pré-Projeto:** A Fintech aprovava limites de empréstimo baseados em análise manual humana e regras de negócio estáticas (ex: se renda for maior que X, aprova Y). Esse processo era lento, engessado e enviesado.
- **Custo da Inação:** A esteira de aprovação tradicional deixava passar um número considerável de fraudadores ou clientes superendividados (cerca de 8% da base), gerando um rombo financeiro silencioso a cada novo ciclo de concessão. 
- **Alinhamento Estratégico:** A diretoria de Risco e Crédito demandou a construção de um **Motor de Inteligência Artificial** capaz de processar o histórico comportamental de +30.000 clientes e predizer a probabilidade matemática de inadimplência no momento exato em que o cliente solicita o dinheiro.

---

### 🔬 3. Metodologia Científica e Técnica (CRISP-DM)
- **Entendimento e Avaliação de Dados (Data Understanding):** 
  - A base de dados principal continha 122 variáveis demográficas, financeiras e comportamentais de ~30.000 clientes.
  - O dataset era **severamente desbalanceado** (92% Bons Pagadores, 8% Inadimplentes), exigindo técnicas robustas de modelagem para evitar o "Paradoxo da Acurácia".
- **Preparação e Engenharia de Dados (Data Preparation):**
  - **ELT Moderno:** Dados brutos foram ingeridos no banco transacional **Supabase (PostgreSQL)**, extraídos via API Python customizada, e carregados no **Google BigQuery** (Data Warehouse).
  - **Camada Semântica:** O **dbt (data build tool)** orquestrou as transformações analíticas, higienizando os dados, removendo nulos e materializando uma OBT (One Big Table) chamada `dim_clientes_credito` pronta para o algoritmo.
- **Modelagem Analítica (Modeling):**
  - O algoritmo escolhido foi o **XGBoost (Extreme Gradient Boosting)**.
  - Implementou-se o balanceamento dinâmico de classes utilizando `scale_pos_weight` calculado pela razão matemática de negativos/positivos (aprox. 11:1), penalizando severamente o algoritmo caso ele aprovasse um mau pagador.
  - *Pipeline de pré-processamento acoplado com StandardScaler e OneHotEncoder.*
- **Avaliação e Garantia de Qualidade (QA / Evaluation):**
  - Validação de Performance: ROC-AUC e Classification Report com foco total na métrica de **Recall da Classe 1** (Prevenção de Falsos Negativos - o calote custa mais caro que perder um cliente bom).

---

### 📈 4. Resultados e Insights Gerados
- **Diagnóstico Oculto:** O modelo revelou que a simples análise de Renda (AMT_INCOME_TOTAL) não é suficiente para aprovar crédito. O padrão de inadimplência está mais atrelado ao comprometimento da renda vs tipo de contrato e idade, fatores que o cérebro humano não correlacionava rápido o suficiente nas planilhas.
- **Ações Imediatas Desencadeadas:** Bloqueio automatizado de clientes localizados no percentil mais arriscado (Score acima de 50%).
- **Impacto Consolidado:** O novo modelo focado em *Recall* consegue pescar **58% dos reais maus pagadores** no ato da simulação. Numa esteira de US$ 17 Milhões concedidos, evitar mais da metade dos calotes traduz-se em retorno líquido massivo.

---

### 🛠️ 5. Plano de Implementação, Governança & Adoção
- **Estratégia de Deploy & Segurança:** 
  - O modelo final foi exportado serializado (`.pkl`) e acoplado numa aplicação web em **Streamlit**.
  - O acesso ao Data Warehouse opera sob chaves de serviço do GCP (*Service Accounts*) com restrições de IAM, protegendo os dados sensíveis dos clientes e atendendo regulamentações (LGPD/GDPR).
- **Matriz de Adoção Operacional (Quem Usa e Como):** 
  - **Analista de Risco / Operador de Mesa:** Usa a aba *Motor Preditivo* para checar CPFs que caem na malha fina ou solicitam valores fora da curva. A ferramenta indica "Negar" ou "Aprovar" de imediato.
  - **Diretor de Crédito (C-Level):** Acessa a aba *Visão Executiva (BI)* para auditar a taxa de default geral e o volume de crédito distribuído, sem precisar tocar em linhas de código.

---

### 🚀 6. Recomendações Estratégicas & Próximos Passos (Roadmap)
- **Recomendações Práticas para o Negócio:**
  - **Alta Prioridade:** Revisar manualmente os clientes classificados como "Risco Moderado" (30% a 50%) para captar clientes bons que foram negados pelo rigor do modelo, utilizando garantias ou taxas de juros mais altas.
  - **Média Prioridade:** Implementar uma taxa flutuante de empréstimo: clientes com risco entre 10% e 20% pagam juros maiores que clientes com risco 1%.
- **Roadmap de Evolução Analítica (Próximos Passos):**
  - **Curto Prazo • 30 Dias (Quick Wins):** Conectar a base do SPC/Serasa via API no modelo.
  - **Médio Prazo • 60-90 Dias (Estruturante):** Automatizar o retreinamento do XGBoost semanalmente via Apache Airflow ou dbt Cloud.
  - **Longo Prazo • 180 Dias (Transformacional):** Mudar a arquitetura para streaming (Pub/Sub + Dataflow) para detectar anomalias transacionais e conceder pequenos créditos recorrentes de forma instantânea.

---

### 📊 7. Decisões Estratégicas C-Level & Perguntas-Chave
- **Audiência Específica:** Diretoria Executiva (CRO/CFO) e Time de Risco Operacional.
- **Perguntas de Negócio Respondidas em Menos de 5 Segundos:**
  1. *Qual é a taxa geral de inadimplência da nossa carteira?* -> **KPI Scorecard: Taxa de Inadimplência (%)**.
  2. *Estamos concentrando calotes em algum gênero ou tipo de contrato?* -> **Gráfico de Barras Agrupadas: Inadimplência por Contrato**.
  3. *Qual o perfil exato do cliente que quer 1 milhão de reais prestes a aprovar?* -> **Motor Preditivo: Input de ID para Score Preditivo Real-time**.
- **Princípios de UX/UI Aplicados:** O Dashboard foi programado em Streamlit com injeções de *Custom CSS* e bibliotecas **Plotly** gráficas em Dark Mode, garantindo leitura amigável, contraste focado (Vermelho para risco, Verde para aprovação) e arquitetura de abas para separar a visão C-Level (Agrupada) da visão do Operador (Individual).
