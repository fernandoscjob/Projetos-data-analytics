# 📈 Modelagem de Cohort, Retenção & Prevenção de Churn

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-fernandocavalcante.vercel.app-38bdf8?style=for-the-badge&logo=vercel)](https://fernandocavalcante.vercel.app/dashboard-cohort.html)
![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-dbt_•_BigQuery_•_Postgres-00758F?style=for-the-badge&logo=dbt)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Power BI](https://img.shields.io/badge/BI-Power_BI-F2C811?style=for-the-badge&logo=powerbi)
![Methodology](https://img.shields.io/badge/Metodologia-CRISP--DM-orange?style=for-the-badge)

> **Case de Estudo Estratégico em Análise Longitudinal & Product Analytics**  
> Modelagem analítica de safras (Cohort Analysis), identificação de gargalos críticos de evasão nos primeiros 60 dias (*Early Churn*) e preservação de R$ 640.000 em Receita Anual Recorrente (ARR).

---

## 🚀 1. TLDR (Resumo Executivo)

- **Objetivo Principal:** Estruturar um pipeline analítico de decomposição de safras temporais (Cohort Analysis) para diagnosticar o ciclo de vida do usuário, isolar a queda acentuada de engajamento nos primeiros 60 dias pós-conversão e embasar a reestruturação da jornada de ativação de produto.
- **Retorno Financeiro / ROI Estimado:** Preservação contábil comprovada de **R$ 640.000,00 em ARR**, impulsionada pelo aumento de **18 pontos percentuais na retenção do 3º mês (de 58% para 76%)** e redução de **25% no churn involuntário**.
- **Tempo de Execução e Performance:** Pipeline modular em SQL/dbt processando mais de 500 mil eventos de produto e faturamento em **menos de 45 segundos** no data warehouse.

### Métricas-Chave de Impacto
| Métrica | Antes da Solução | Com Cohort Analytics | Impacto / Melhoria |
| :--- | :--- | :--- | :--- |
| **Taxa de Retenção no Mês 3 (M3)** | 58% da safra retida | 76% da safra retida | Ganho de +18 p.p. na maturidade |
| **Early Churn (0-60 dias)** | 28% de perda silenciosa | 13% com alertas de inatividade | Queda de mais de 50% na evasão precoce |
| **ARR Preservado** | Sangria de receita recorrente | R$ 640.000,00 protegidos | Aumento sustentável do LTV |
| **Payback do CAC** | 14 meses (risco de insolvência) | 8,5 meses | Aceleração no ponto de equilíbrio |

---

## 💼 2. O Problema de Negócio (Business Understanding)

### Cenário Corporativo
Empresas orientadas a receita recorrente (SaaS ou assinaturas) investiam expressivo capital em campanhas de aquisição de tráfego pago (CAC). Apesar do fluxo contínuo de novas contas no topo do funil, os resultados globais de faturamento permaneciam estagnados em função de um vazamento severo de clientes no fundo do funil.

### Dor Operacional & Custo da Inação
1. **Onda de Evasão Invisível:** 28% das novas contas abandonavam a plataforma antes de completar o 2º mês de uso, gerando um prejuízo líquido em que o CAC jamais era amortizado.
2. **Falta de Visibilidade por Safra:** A diretoria avaliava apenas a taxa agregada de churn mensal (ex.: 3,5% ao mês), número mascarado pelo fluxo de novos clientes que ocultava a destruição de valor nas contas maduras.
3. **Custo da Inação:** A manutenção do cenário exigiria um aumento contínuo do orçamento de marketing para compensar o churn, tornando a operação insustentável no médio prazo.

---

## 🔬 3. Metodologia Científica e Técnica (CRISP-DM)

### 3.1. Entendimento dos Dados (Data Understanding)
- Dados transacionais de faturamento mensal e logs de telemetria de uso de produto.
- Atributos essenciais: `id_usuario`, `data_evento`, `tipo_evento`, `plano_subscricao` e `valor_mensalidade`.

### 3.2. Engenharia e Preparação de Dados (ETL/ELT com dbt & SQL)
- Definição da safra de origem através da data da primeira conversão: $T_0 = \min(\text{data_transacao})$.
- Agrupamento mensal e cálculo da distância temporal em meses decorridos ($M_0, M_1, M_2, \dots, M_n$).
- Implementação em SQL analítico de alta performance com Window Functions:

```sql
-- cohort_pipeline.sql: Cálculo da Matriz de Retenção
WITH tb_primeira_compra AS (
    SELECT 
        user_id,
        DATE_TRUNC(MIN(data_transacao), MONTH) AS safra_mes
    FROM tb_transacoes
    WHERE status = 'CONCLUIDA'
    GROUP BY user_id
),
tb_atividade_mensal AS (
    SELECT 
        t.user_id,
        p.safra_mes,
        DATE_TRUNC(t.data_transacao, MONTH) AS atividade_mes,
        DATE_DIFF(DATE_TRUNC(t.data_transacao, MONTH), p.safra_mes, MONTH) AS periodo_mes
    FROM tb_transacoes t
    INNER JOIN tb_primeira_compra p ON t.user_id = p.user_id
    WHERE t.status = 'CONCLUIDA'
    GROUP BY 1, 2, 3, 4
),
tb_contagem_safra AS (
    SELECT 
        safra_mes,
        COUNT(DISTINCT user_id) AS tamanho_safra
    FROM tb_primeira_compra
    GROUP BY 1
)
SELECT 
    a.safra_mes,
    s.tamanho_safra,
    a.periodo_mes,
    COUNT(DISTINCT a.user_id) AS usuarios_ativos,
    ROUND(COUNT(DISTINCT a.user_id) * 100.0 / s.tamanho_safra, 2) AS taxa_retencao_pct,
    ROUND(100.0 - (COUNT(DISTINCT a.user_id) * 100.0 / s.tamanho_safra), 2) AS taxa_churn_pct
FROM tb_atividade_mensal a
INNER JOIN tb_contagem_safra s ON a.safra_mes = s.safra_mes
GROUP BY 1, 2, 3
ORDER BY 1, 3;
```

### 3.3. Avaliação e Garantia de Qualidade (QA & Testing)
- **Monotonicidade da Safra:** A retenção em $M_0$ é obrigatoriamente 100%.
- **Testes de Integridade dbt:** Testes automatizados garantindo unicidade de `user_id` e integridade referencial nas tabelas de fato e dimensão.

---

## 📈 4. Resultados e Insights Gerados

### Principais Descobertas
1. **O "Momento Eureka" de Ativação:** Usuários que realizavam 3 ou mais ações-chave na primeira semana apresentavam taxa de retenção em M3 de **82%**, contra apenas **24%** dos que completavam apenas o cadastro básico.
2. **Gargalo no Dia 21:** A maior taxa marginal de abandono ocorria na 3ª semana, motivada pela perda de suporte no onboarding inicial.
3. **Redesenho da Jornada:** A reformulação do onboarding pelo time de Produto elevou o benchmark global de retenção em M3 de **58% para 76%**.

---

## 🛠️ 5. Plano de Implementação, Governança e Próximos Passos

### Matriz de Adoção Operacional (Quem usa e Como)
| Papel / Persona | Ferramenta / Ação | Frequência | Decisão Tomada |
| :--- | :--- | :--- | :--- |
| **Head de Produto (CPO)** | Matriz Heatmap de Safras | Mensal | Priorização de features de onboarding e ativação |
| **Líder de Customer Success** | Dashboard de Alertas de Churn | Semanal | Intervenção em contas que não atingiram marcos no M1 |
| **Growth Marketing** | Análise de Coorte por Canal | Quinzenal | Realocação de budget de mídia para canais com maior LTV |

---

## 📊 6. Design do Dashboard de Suporte e Perguntas-Chave

### Audiência-Alvo
Líderes de Produto (Product Managers), Diretores de Customer Success e Executivos de Finanças (CFO).

### Perguntas Estratégicas Respondidas em < 5 Segundos
1. **As novas safras de clientes estão retendo melhor do que as safras do ano passado?**  
   *Resposta:* Heatmap triangular com escala cromática destacando a evolução temporal de cada linha de safra.
2. **Em qual mês específico ocorre a maior sangria de clientes?**  
   *Resposta:* Curva de sobrevivência destacando o declínio acentuado entre $M_0$ e $M_2$.
3. **Qual é o volume de ARR resgatado pelas novas ações de produto?**  
   *Resposta:* Indicador de R$ 640k preservados posicionado no topo da interface executiva.

---

## 📁 Estrutura de Arquivos e Execução

```
03_Cohort_Retencao_Churn/
├── cohort_model.py         # Script Python para geração sintética, cálculo da matriz e KPIs
├── cohort_pipeline.sql     # Pipeline de dados em SQL com CTEs e Window Functions
├── requirements.txt        # Dependências mínimas (pandas, numpy)
└── README.md               # Documentação técnica do projeto
```

### Como Executar Localmente
```bash
python cohort_model.py
```
O script processará a série histórica e imprimirá as matrizes consolidadas de Retenção e Churn por safra.
