# 🏛️ Camada Semântica Corporativa, Modelagem Dimensional & Cockpit Executivo

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![dbt](https://img.shields.io/badge/Modeling-dbt_Core-FF694B?style=for-the-badge&logo=dbt)
![Power BI](https://img.shields.io/badge/BI-Power_BI_(DAX)-F2C811?style=for-the-badge&logo=powerbi)
![Data Governance](https://img.shields.io/badge/Governance-SSOT_•_RLS-10B981?style=for-the-badge)

Arquitetura de modelagem dimensional baseada no framework **Kimball (Star Schema)** e implantação de uma **Camada Semântica Centralizada (Single Source of Truth - SSOT)** para eliminação de divergências contábeis entre áreas de negócio e suporte a 120+ decisores.

---

## 💼 Contexto de Negócio & Desafio

Divergência crônica entre os relatórios da área Comercial e da Controladoria:
- **Vendas** reportava receita com base em pedidos emitidos.
- **Finanças** reportava receita com base em faturamento líquido e baixas contábeis.
- Reuniões de diretoria perdiam tempo discutindo a veracidade dos números ao invés de definir estratégias de crescimento.

**Resultados Mensurados:**
- **Fonte única da verdade (SSOT)** adotada por 100% da diretoria e gestores.
- Fechamento mensal acelerado de 5 dias úteis para **visualização em D-0**.
- Identificação de 3 linhas de produtos com margem líquida negativa, possibilitando ajuste imediato de precificação.

---

## 🧠 Arquitetura Dimensional (Star Schema)

- **Fato Incremental (`fct_vendas`):** Particionada mensalmente por data de emissão e clusterizada por cliente e produto para máxima eficiência de custo em queries.
- **Dimensões Conformadas:**
  - `dim_clientes`: Cadastro unificado de contas corporativas.
  - `dim_produtos`: Hierarquia de categorias e custos padrão.
  - `dim_calendario`: Dimensão tempo com ano fiscal e dias úteis.
- **Biblioteca DAX Padronizada:** 14 medidas corporativas imutáveis (Receita Líquida, CMV, Margem de Contribuição, Ticket Médio, MoM Growth).

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
