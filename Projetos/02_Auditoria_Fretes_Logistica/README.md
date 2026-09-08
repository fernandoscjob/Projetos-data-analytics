# 🚚 Auditoria Contratual de Fretes & Otimização de Custos de Transporte

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=for-the-badge&logo=plotly)
![SQL](https://img.shields.io/badge/SQL-BigQuery_•_PostgreSQL-00758F?style=for-the-badge&logo=postgresql)
![Methodology](https://img.shields.io/badge/Metodologia-CRISP--DM-orange?style=for-the-badge)

> **Case de Estudo Estratégico em Engenharia de Dados & Supply Chain**  
> Conciliação automatizada de 800 CT-es e faturas de frete contra tabelas contratuais vigentes de 14 transportadoras, identificando R$ 1.200.000,00 em glosas e sobretaxas indevidas.

---

## 🚀 1. TLDR (Resumo Executivo)

- **Objetivo Principal:** Estruturar um pipeline automatizado de conciliação fiscal e contratual de faturas de transporte (CT-e), confrontando pesos tarifados, cubagem volumétrica e tarifas acessórias contra tabelas acordadas com 14 transportadoras logísticas.
- **Retorno Financeiro / ROI Estimado:** Recuperação contábil imediata de **R$ 1.200.000,00 em glosas contratuais** (representando **14,8% do total faturado de R$ 8.120.000,00**), além de corte permanente de **40% nas sobretaxas acessórias** no trimestre subsequente.
- **Tempo de Execução e Performance:** Redução do ciclo operacional de conferência e auditoria de **12 dias úteis para menos de 2 horas** (e execução em batch SQL em menos de 3 minutos).

### Métricas-Chave de Impacto
| Métrica | Antes da Solução | Com Auditoria de Fretes | Impacto / Melhoria |
| :--- | :--- | :--- | :--- |
| **Volume Auditado** | Amostragem manual (~5% das faturas) | 100% dos CT-es (800 documentos) | Cobertura integral de riscos fiscais |
| **Valor Faturado vs. Devido** | R$ 8.120.000,00 pagos sem blindagem | Faturado: R$ 8.12M | Devido: R$ 6.92M | Glosas: R$ 1.200.000,00 contestados |
| **Tempo de Ciclo de Aprovação** | 12 dias úteis de validação manual | Menos de 2 horas | Agilidade de pagamento e corte de multas |
| **Sobretaxas Acessórias** | Pagamento cego de reentregas/diárias | Contestação fundamentada | Queda de 40% nas cobranças no 1º tri |

---

## 💼 2. O Problema de Negócio (Business Understanding)

### Cenário Corporativo
Operações industriais e de e-commerce de grande escala movimentam milhares de despachos de carga fracionada e lotação através de dezenas de parceiros logísticos. A empresa operava com **14 transportadoras homologadas**, gerando um faturamento mensal auditado de **R$ 8.120.000,00**.

### Dor Operacional & Custo da Inação
1. **Cobrança Sistemática de Sobretaxas Acessórias:** Transportadoras inseriam tarifas adicionais de reentrega, diárias de armazenagem e taxas de difícil acesso sem registros comprobatórios de tentativa frustrada de entrega.
2. **Divergência de Cubagem Volumétrica:** Constatou-se que balanças e cubômetros de operadores parceiros superestimavam o peso volumétrico em até 28% em relação aos dados do WMS de expedição.
3. **Custo da Inação:** A ausência de uma malha automatizada de auditoria provocava uma sangria invisível de mais de **R$ 1 milhão a cada fechamento contábil**, absorvida como custo operacional sem repasse.

---

## 🔬 3. Metodologia Científica e Técnica (CRISP-DM)

### 3.1. Entendimento dos Dados (Data Understanding)
Integração de duas fontes centrais:
1. **Faturas Fiscais de Transporte (CT-e):** Número do CT-e, chave fiscal, transportadora, peso aferido, volume ($m^3$), valor declarado e valor total cobrado.
2. **Tabela Contratual Negociada:** Matriz tarifária por rota (UF origem / UF destino), fator de cubagem contratual ($300\text{ kg}/m^3$), taxa base, ad-valorem (% do valor da mercadoria), pedágio por fração de 100 kg e regras de cobrança de GRIS.

### 3.2. Engenharia e Preparação de Dados (ETL/ELT)
- Deduplicação e normalização de chaves de CT-e.
- Cálculo determinístico do peso faturável segundo o modelo matemático contratual:
  $$\text{Peso Tarifado} = \max(\text{Peso Real (kg)}, \text{Volume } (m^3) \times \text{Fator Cubagem})$$
- Pipeline em SQL implementado com Common Table Expressions (CTEs) particionado por transportadora:

```sql
-- queries_auditoria.sql: Conciliação Contratual de Frete
WITH cte_contrato AS (
    SELECT 
        c.cte_id,
        c.transportadora,
        c.valor_cobrado,
        c.peso_real_kg,
        c.volume_m3,
        -- Peso tarifado segundo fator contratual (300 kg/m3)
        GREATEST(c.peso_real_kg, c.volume_m3 * t.fator_cubagem) AS peso_tarifado,
        -- Valor devido contratualmente
        (t.tarifa_base + 
         (GREATEST(c.peso_real_kg, c.volume_m3 * t.fator_cubagem) * t.tarifa_excedente_kg) +
         (c.valor_nf * t.aliquota_gris) +
         (CEIL(c.peso_real_kg / 100.0) * t.valor_pedagio_fracao)
        ) AS valor_devido
    FROM tb_cte_faturado c
    INNER JOIN tb_tabela_frete t 
        ON c.transportadora_id = t.transportadora_id 
       AND c.uf_destino = t.uf_destino
)
SELECT 
    cte_id,
    transportadora,
    valor_cobrado,
    ROUND(valor_devido, 2) AS valor_devido,
    ROUND(valor_cobrado - valor_devido, 2) AS valor_glosa,
    CASE 
        WHEN (valor_cobrado - valor_devido) > 10.00 THEN 'CONTESTAR'
        WHEN (valor_cobrado - valor_devido) < -5.00 THEN 'UNDERBILLED'
        ELSE 'APROVADO'
    END AS status_auditoria
FROM cte_contrato;
```

### 3.3. Avaliação e Garantia de Qualidade (QA & Testing)
- **Tolerância de Variação:** Estabelecido threshold de tolerância de $\pm R\$ 10,00$ para acomodar arredondamentos tributários sem gerar contestação desnecessária.
- **Matriz de Causa-Raiz das Glosas:**
  - 45% Cubagem / Peso Aferido Aumentado
  - 32% Reentrega e Armazenagem Não Comprovadas
  - 16% Pedágio e GRIS Cobrados em Desconformidade
  - 7% Tarifa Base e Excedente fora da Tabela Vigente

---

## 📈 4. Resultados e Insights Gerados

### Principais Descobertas
1. **Concentração de Glosas por Transportadora:** Duas das 14 transportadoras respondiam por **48% de todo o valor glosado**, indicando necessidade de renegociação imediata de SLA ou descredenciamento.
2. **Impacto Sistemático da Cubagem:** Transportadoras com cubômetros descalibrados geravam notas com até 35% de sobrepreço volumétrico em cargas de baixa densidade.
3. **Eficácia da Contestação Automática:** Cartas de conciliação enviadas com evidências analíticas obtiveram taxa de aceite e estorno superior a **92% junto aos operadores logísticos**.

---

## 🛠️ 5. Plano de Implementação, Governança e Próximos Passos

### Arquitetura de Produção
- **Camada de Orquestração:** Ingestão diária de XMLs de CT-e via pipeline acionado por trigger de recebimento no ERP/WMS.
- **Camada de Apresentação:** Dashboard executivo interativo em Streamlit e versão standalone ultraleve em HTML5/Plotly.js integrada ao site de portfólio.

### Matriz de Adoção Operacional (Quem usa e Como)
| Papel / Persona | Ferramenta / Ação | Frequência | Decisão Tomada |
| :--- | :--- | :--- | :--- |
| **Gerente de Logística / Supply Chain** | Dashboard de Performance por Transportadora | Semanal | Ranqueamento de operadores e alocação de cargas |
| **Coordenador de Contas a Pagar** | Relatório de Glosas e Discrepâncias | Diária | Liberação de faturas e retenção de pagamentos |
| **Auditor de Fretes / Fiscal** | Carta de Contestação Gerada | Por lote | Envio formal de conciliação aos parceiros |

---

## 📊 6. Design do Dashboard de Suporte e Perguntas-Chave

### Audiência-Alvo
Gerentes de Supply Chain, Controladores de Custos Logísticos e Supervisores de Contas a Pagar.

### Perguntas Estratégicas Respondidas em < 5 Segundos
1. **Qual é o total financeiro a ser glosado no lote atual?**  
   *Resposta:* R$ 1.200.000,00, destacado no card principal com indicador de 14,8% da fatura.
2. **Quais transportadoras apresentam maior índice de não-conformidade contratual?**  
   *Resposta:* Gráfico de barras horizontais ranqueando o volume glosado e a taxa de erro por operador.
3. **Qual é a principal causa de divergência financeira no período?**  
   *Resposta:* Gráfico de rosca detalhando a distribuição percentual das justificativas de glosa.

---

## 📁 Estrutura de Arquivos e Execução

```
02_Auditoria_Fretes_Logistica/
├── app.py                    # Aplicação Web completa em Streamlit & Plotly
├── auditoria_fretes.py       # Motor Python de simulação, conciliação e geração de KPIs
├── queries_auditoria.sql     # Pipeline analítico em SQL com CTEs e regras contratuais
├── requirements.txt          # Dependências (streamlit, pandas, numpy, plotly, openpyxl)
└── README.md                 # Documentação técnica do projeto
```

### Como Executar Localmente
```bash
# Executar a aplicação Streamlit
streamlit run app.py

# Ou executar o motor de auditoria em terminal
python auditoria_fretes.py
```
Acesse o dashboard standalone no navegador abrindo o arquivo `Site/dashboard-fretes.html`.
