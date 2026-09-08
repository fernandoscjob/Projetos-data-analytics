# 📈 Modelagem de Cohort, Retenção & Prevenção de Churn

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-dbt_•_BigQuery_•_Postgres-00758F?style=for-the-badge&logo=dbt)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Power BI](https://img.shields.io/badge/BI-Power_BI-F2C811?style=for-the-badge&logo=powerbi)

Modelagem de dados analítica de Safras (Cohort Analytics) para mapear o ciclo de vida dos clientes, quantificar o *Early Churn* (evasão precoce nos primeiros 60 dias) e subsidiar ações proativas de retenção para os times de Produto e Customer Success.

---

## 💼 Contexto de Negócio & Desafio

A empresa possuía um volume consistente de aquisição no topo de funil, porém sofria com **28% de evasão silenciosa nos primeiros 60 dias** pós-conversão:
- O CAC (Custo de Aquisição de Clientes) demorava mais de 14 meses para atingir o Payback.
- Clientes com baixa ativação na 2ª e 3ª semana abandonavam a plataforma sem que o time de CS percebesse.

**Resultados Mensurados:**
- **+18 p.p.** de aumento na taxa de retenção em M3 (de 58% para 76%) com a reformulação do onboarding orientada por dados.
- **25% de redução** no churn involuntário via alertas proativos de inatividade.
- **R$ 640.000 preservados** em Annual Recurring Revenue (ARR).

---

## 🧠 Metodologia de Safras (Cohort Logic)

1. **Atribuição First-Touch:** Agrupamento de clientes pela data da primeira transação (`MIN(data_compra)`).
2. **Matriz Temporal Longitudinal:** Cálculo da diferença em meses ($M_0, M_1, \dots, M_n$) entre a safra e cada compra subsequente.
3. **Curva de Sobrevivência (Survival Rate):**
   $$\text{Taxa Retenção } (M_i) = \frac{\text{Clientes Ativos em } M_i}{\text{Total de Clientes na Safra } M_0} \times 100$$
   $$\text{Taxa Churn } (M_i) = 100\% - \text{Taxa Retenção } (M_i)$$

---

## 📁 Estrutura de Arquivos

```
03_Cohort_Retencao_Churn/
├── cohort_model.py         # Script Python para geração sintética, cálculo da matriz e KPIs
├── cohort_pipeline.sql     # Pipeline de dados em SQL com CTEs e Window Functions
├── requirements.txt        # Dependências mínimas (pandas, numpy)
└── README.md               # Documentação técnica do projeto
```

---

## 🚀 Como Executar Localmente

```bash
cd Projetos/03_Cohort_Retencao_Churn
python cohort_model.py
```
O script exibirá no console a **Matriz de Retenção (%)**, a **Matriz de Churn (%)** e as métricas médias dos primeiros meses.
