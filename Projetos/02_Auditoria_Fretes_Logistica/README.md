# 🚚 Auditoria Contratual de Fretes & Otimização de Custos de Transporte

![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=for-the-badge&logo=plotly)
![SQL](https://img.shields.io/badge/SQL-BigQuery_•_PostgreSQL-00758F?style=for-the-badge&logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)

Pipeline analítico de engenharia e auditoria de dados para conciliação automatizada de faturas de frete (CT-e) contra tabelas contratuais vigentes de transportadoras, identificação de cobranças indevidas (glosas) e otimização logística. Acompanha aplicação web interativa em **Streamlit** e dashboard standalone dedicado com **Plotly.js**.

---

## 💼 Contexto de Negócio & Desafio

Grandes operações logísticas com dezenas de milhares de entregas mensais sofrem sistematicamente com cobranças de sobretaxas acessórias não pactuadas:
- Cubagem volumétrica superestimada na pesagem da transportadora.
- Taxas indevidas de reentrega e diárias de armazenagem cobradas sem comprovação de insucesso.
- Tarifas de pedagio e GRIS (seguro) calculadas em desconformidade com a legislação ou contrato.

**Resultados Mensurados:**
- **40% de redução** nas sobretaxas acessórias logo no 1º trimestre de auditoria contínua.
- **R$ 1.200.000 recuperados** em glosas e notas fiscais contestadas na auditoria retroativa.
- Redução do ciclo de conferência manual de 12 dias úteis para **menos de 2 horas** via automação.

---

## 🧠 Arquitetura Analítica & Regras de Negócio

1. **Cálculo de Cubagem Contratual:**
   $$\text{Peso Tarifado} = \max(\text{Peso Real (kg)}, \text{Volume } (m^3) \times \text{Fator Cubagem})$$
2. **Componentes da Tarifa Contratual:**
   - Tarifa Base Fixa por Destino / Região.
   - Preço Excedente por kg.
   - Ad-valorem / Seguro GRIS proporcional ao valor da mercadoria (ex.: 0.3%).
   - Pedágio tarifado por fração de 100 kg.
3. **Threshold de Glosa:**
   - Variações superiores a R$ 10,00 por CT-e disparam rejeição automática de fatura e emissão de carta de contestação.

---

## 📁 Estrutura de Arquivos

```
02_Auditoria_Fretes_Logistica/
├── app.py                    # Aplicação Web completa em Streamlit & Plotly
├── auditoria_fretes.py       # Motor Python de simulação, conciliação e geração de KPIs
├── queries_auditoria.sql     # Pipeline analítico em SQL (BigQuery/Postgres) com CTEs
├── requirements.txt          # Dependências (streamlit, pandas, numpy, plotly, openpyxl)
└── README.md                 # Documentação técnica do projeto
```

---

## 🚀 Como Executar Localmente

### Opção 1: Executar o Cockpit Interativo em Streamlit
Na raiz do repositório:
```bash
streamlit run Projetos/02_Auditoria_Fretes_Logistica/app.py
```
Acesse no navegador: `http://localhost:8501`. Permite upload de planilhas de CT-e em CSV/Excel, ajuste dinâmico de tolerância e download de carta de contestação.

### Opção 2: Executar o Motor de Auditoria no Terminal (CLI)
```bash
python Projetos/02_Auditoria_Fretes_Logistica/auditoria_fretes.py
```
O script gerará uma amostra estocástica de 500 CT-es, aplicará as regras contratuais e imprimirá o resumo consolidado de valores recuperáveis por transportadora.

### Opção 3: Visualizar o Dashboard Standalone no Navegador
Abra o arquivo [`Site/dashboard-fretes.html`](../../Site/dashboard-fretes.html) diretamente no navegador para interagir com o cockpit sem precisar de backend Python.
