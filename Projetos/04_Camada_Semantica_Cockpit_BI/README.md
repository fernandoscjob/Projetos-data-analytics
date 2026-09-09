# 🏛️ Camada Semântica Corporativa, Modelagem Dimensional & Cockpit Executivo

[![Live Dashboard](https://img.shields.io/badge/Live_Dashboard-fernandocavalcante.vercel.app-38bdf8?style=for-the-badge&logo=vercel)](https://fernandocavalcante.vercel.app/dashboard-bi.html)
![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![dbt](https://img.shields.io/badge/Modeling-dbt_Core-FF694B?style=for-the-badge&logo=dbt)
![Power BI](https://img.shields.io/badge/BI-Power_BI_(DAX)-F2C811?style=for-the-badge&logo=powerbi)
![Data Governance](https://img.shields.io/badge/Governance-SSOT_•_RLS-10B981?style=for-the-badge)
![Methodology](https://img.shields.io/badge/Metodologia-CRISP--DM-orange?style=for-the-badge)

> **Case de Estudo Estratégico em Engenharia Analítica & Governança de Dados**  
> Implementação de arquitetura dimensional Kimball (Star Schema), governança métrica unificada (SSOT) para 120+ tomadores de decisão e proteção anual de R$ 380.000 em margem operacional.

---

## 🚀 1. TLDR (Resumo Executivo)

- **Objetivo Principal:** Eliminar a fragmentação de indicadores financeiros e comerciais na organização mediante a criação de uma Camada Semântica Corporativa padronizada com dbt e Power BI, implementando uma modelagem dimensional Star Schema de alta performance e segurança por linha (Row-Level Security).
- **Retorno Financeiro / ROI Estimado:** Proteção de **R$ 380.000,00/ano em margem líquida** a partir da identificação imediata de 3 linhas de produtos com margem de contribuição negativa, além da **eliminação de 5 dias úteis de espera** no fechamento mensal (D-0 em tempo real).
- **Tempo de Execução e Performance:** Redução de **68% na latência de execução de consultas** analíticas no data warehouse através de particionamento e pré-agregações dimensionais.

### Métricas-Chave de Impacto
| Métrica | Antes da Solução | Com Camada Semântica & SSOT | Impacto / Melhoria |
| :--- | :--- | :--- | :--- |
| **Consistência de Métricas** | Relatórios divergentes (Vendas vs Finanças) | Fonte Única da Verdade (SSOT) | 100% de alinhamento executivo |
| **Tempo de Fechamento Contábil** | 5 dias úteis de conciliação manual | D-0 em tempo real | Decisão ágil no primeiro dia do mês |
| **Margem Líquida Protegida** | Produtos deficitários ocultos | 3 linhas corrigidas | R$ 380.000,00/ano em economia |
| **Usuários Concorrentes Atendidos** | Relatórios locais lentos | 120+ decisores conectados via RLS | Governança e segurança corporativa |

---

## 💼 2. O Problema de Negócio (Business Understanding)

### Cenário Corporativo
A empresa possuía mais de 120 tomadores de decisão distribuídos entre Vendas, Marketing, Controladoria e Operações. No entanto, a tomada de decisão estratégica era constantemente paralisada por disputas em torno da precisão das planilhas apresentadas nas reuniões de diretoria.

### Dor Operacional & Custo da Inação
1. **Guerra de Planilhas:** A área de Vendas comemorava recorde de vendas considerando pedidos emitidos brutos, enquanto a Controladoria reportava queda na receita considerando devoluções, cancelamentos e impostos incidentes.
2. **Falta de Governança e RLS:** Informações estratégicas de margem e precificação trafegavam livremente em arquivos locais sem controle de permissões por perfil ou filial.
3. **Custo da Inação:** A inércia no fechamento mensal atrasava decisões de precificação, permitindo que produtos deficitários continuassem sendo comercializados por meses com margem negativa.

---

## 🔬 3. Metodologia Científica e Técnica (CRISP-DM)

### 3.1. Entendimento dos Dados & Modelagem Kimball (Star Schema)
Estruturação de um modelo dimensional estrito para eliminar redundâncias e garantir performance máxima:
- **Tabela Fato Incremental (`fct_vendas`):** Grão de item vendido, contendo métricas transacionais aditivas (quantidade, valor bruto, desconto, impostos, custo dos produtos vendidos).
- **Dimensões Conformadas:**
  - `dim_clientes`: Cadastro unificado e histórico de clientes.
  - `dim_produtos`: Hierarquia de categorias, marcas e custos padrão.
  - `dim_calendario`: Dimensão temporal enriquecida com calendário fiscal e dias úteis.

### 3.2. Engenharia e Governança Semântica (dbt + DAX)
- Padronização corporativa de **14 medidas analíticas fundamentais**, imutáveis e auditadas:

```dax
-- Catálogo de Medidas Corporativas (SSOT)

-- 1. Faturamento Líquido
Receita_Liquida = 
SUMX(
    fct_vendas, 
    fct_vendas[valor_bruto] - fct_vendas[valor_desconto] - fct_vendas[valor_impostos]
)

-- 2. Margem de Contribuição (%)
Margem_Contribuicao_Pct = 
VAR _Receita = [Receita_Liquida]
VAR _CMV = SUM(fct_vendas[custo_mercadoria_vendida])
RETURN
DIVIDE(_Receita - _CMV, _Receita, 0)

-- 3. Crescimento MoM (Month-over-Month)
Receita_MoM_Growth = 
VAR _MesAtual = [Receita_Liquida]
VAR _MesAnterior = CALCULATE([Receita_Liquida], DATEADD(dim_calendario[data], -1, MONTH))
RETURN
DIVIDE(_MesAtual - _MesAnterior, _MesAnterior, 0)
```

### 3.3. Avaliação, Segurança e RLS
- **Row-Level Security (RLS):** Criação de papéis de segurança dinâmica no Power BI (`USERPRINCIPALNAME()`) garantindo que gerentes regionais visualizem exclusivamente as vendas da sua diretoria, enquanto a C-Suite possui visão consolidada.

---

## 📈 4. Resultados e Insights Gerados

### Principais Descobertas
1. **Descoberta de Linhas Deficitárias:** A segregação precisa do CMV revelou 3 linhas de produtos com margem de contribuição negativa (-4,2%), permitindo reajuste de preço e economia imediata de R$ 380k/ano.
2. **Eliminação do retrabalho:** As equipes de Controladoria e Vendas deixaram de gastar 40 horas mensais gerando relatórios paralelos no Excel.

---

## 🛠️ 5. Plano de Implementação, Governança e Próximos Passos

### Matriz de Adoção Operacional (Quem usa e Como)
| Papel / Persona | Ferramenta / Ação | Frequência | Decisão Tomada |
| :--- | :--- | :--- | :--- |
| **C-Level (CEO / CFO / COO)** | Cockpit Executivo Consolidado | Diária | Monitoramento de metas globais e margem líquida |
| **Gerentes Comerciais Regionais** | Visão Filtrada via RLS | Diária | Acompanhamento de metas de representantes e filiais |
| **Controladoria e Planejamento** | Análise Detalhada de Custos e CMV | Mensal | Validação de custos padrão e política fiscal |

---

## 📊 6. Design do Dashboard de Suporte e Perguntas-Chave

### Audiência-Alvo
Diretoria Executiva (C-Suite) e Gerentes Regionais de Negócio.

### Perguntas Estratégicas Respondidas em < 5 Segundos
1. **A empresa atingiu a meta de margem de contribuição no mês corrente?**  
   *Resposta:* Cartão KPI comparando a margem real contra o target com coloração dinâmica.
2. **Quais filiais estão abaixo do ponto de equilíbrio operacional?**  
   *Resposta:* Gráfico de dispersão cruzando volume vendido versus margem de contribuição por regional.
3. **Qual é o impacto das devoluções na receita bruta?**  
   *Resposta:* Gráfico de cascata (Waterfall chart) demonstrando a conciliação da receita bruta à receita líquida.

---

## 📁 Estrutura de Arquivos

```
04_Camada_Semantica_Cockpit_BI/
├── dbt_models/
│   ├── dim_clientes.sql              # Dimensão conformada de clientes
│   ├── dim_produtos.sql              # Dimensão de produtos e categorias
│   ├── dim_calendario.sql            # Dimensão temporal com atributos fiscais
│   ├── fct_vendas.sql                # Tabela fato incremental de vendas
│   └── schema.yml                    # Contratos de dados e testes de integridade dbt
├── medidas_dax_corporativas.dax      # Catálogo de medidas DAX padronizadas
└── README.md                         # Documentação técnica da arquitetura
```
