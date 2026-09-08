# 🎯 Cockpit Analítico RFM & Prevenção de Churn em Vendas

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-5.18%2B-3F4F75?style=for-the-badge&logo=plotly)

Aplicação analítica executiva desenvolvida em **Python**, **Streamlit** e **Plotly** para diagnóstico de carteira de clientes, identificação de receita em risco de evasão (churn) e geração de playbooks táticos acionáveis para os times de **Customer Success (CS)** e **Vendas**.

---

## 💼 Desafio de Negócio

Em modelos de vendas recorrentes e B2B/B2C, um dos maiores gargalos é a **abordagem homogênea da carteira**:
- Clientes com histórico de alto faturamento (VIPs) entram em inatividade silenciosa sem alertas prévios.
- Clientes recentes recebem a mesma régua promocional que compradores esporádicos.
- Equipes comerciais perdem tempo contatando contas de baixo retorno enquanto a receita em risco evade.

**Impacto mensurado:** Neste diagnóstico, foram mapeados **R$ 485.200 (24,8% da receita global)** concentrados em contas com sinais iminentes de perda (*Não Podemos Perder* e *Em Risco*).

---

## 🧠 Metodologia RFM & Engenharia de Dados

O modelo processa o histórico transacional agrupando os dados no nível de cliente e calculando três pilares:

| Pilar | Definição | Métrica |
| :--- | :--- | :--- |
| **Recência (R)** | Dias transcorridos desde a última compra até a data de corte. | Menor é melhor (score 5 = mais recente). |
| **Frequência (F)** | Quantidade de compras/pedidos únicos realizados no período. | Maior é melhor (score 5 = mais pedidos). |
| **Valor Monetário (M)** | Soma financeira total faturada com o cliente no período. | Maior é melhor (score 5 = maior faturamento). |

### Desempate Estatístico com Quantis (`pd.qcut`)
Em transações reais, empates na frequência (ex.: múltiplos clientes com apenas 1 pedido) quebram divisões simples por quantis. Para garantir rigor estatístico sem distorções, utilizamos o método ordinal de primeiro desempate:

```python
rfm['R_Score'] = pd.qcut(rfm['Recencia'].rank(method='first'), q=5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequencia'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Valor'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
```

---

## 🏷️ Matriz dos 11 Clusters Estratégicos

Cada cliente é alocado determinística e exclusivamente em um dos 11 segmentos:

1. **Campeões** (`R 4-5`, `F 4-5`, `M 4-5`): Seus melhores clientes. Compram com frequência e alto ticket.
2. **Clientes Leais** (`R 3-5`, `F 3-5`, `M 3-5`): Compram regularmente e são receptivos a promoções.
3. **Potenciais Leais** (`R 4-5`, `F 2-3`): Compras recentes com boa frequência; potenciais novos campeões.
4. **Novos Clientes** (`R 4-5`, `F <= 1`): Compraram recentemente pela primeira vez.
5. **Promissores** (`R 3-4`, `F <= 1`): Compradores recentes que necessitam de incentivo para a 2ª compra.
6. **Precisam de Atenção** (`R 3`, `F 2-3`, `M 2-4`): Acima da média, mas a recência começou a cair.
7. **Quase Hibernando** (`R 2-3`, `F 1-2`, `M 1-3`): Baixa frequência e sem compras há algum tempo.
8. **Em Risco** (`R 1-2`, `F 2-5`, `M 3-5`): Gastavam muito e compravam com frequência, mas estão inativos!
9. **Não Podemos Perder** (`R 1-2`, `F 4-5`, `M 4-5`): Maiores clientes históricos com recência crítica. Alerta vermelho!
10. **Hibernando** (`R 1-2`, `F 1-2`, `M 1-2`): Baixo valor e inativos há meses.
11. **Perdidos** (`R 1`, `F 1`, `M 1`): Menor recência, frequência e valor histórico.

---

## 📁 Estrutura de Arquivos deste Projeto

```
01_Cockpit_RFM_Analytics/
├── app.py              # Interface executiva completa em Streamlit
├── rfm_engine.py       # Módulo Python com gerador sintético, quantis e regras de clusters
├── requirements.txt    # Dependências do projeto (streamlit, pandas, numpy, plotly, openpyxl)
└── README.md           # Documentação técnica do projeto
```

---

## 🚀 Como Executar

### 1. Pré-requisitos
Certifique-se de ter o Python 3.10 ou superior instalado.

### 2. Instalação das Dependências
Na pasta deste projeto, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
```

### 3. Execução da Aplicação
Execute o comando do Streamlit:
```bash
streamlit run app.py
```
Acesse no seu navegador: `http://localhost:8501`.

---

## 🌟 Funcionalidades da Aplicação

- **Modo Demonstração ou Upload Real**: Caso nenhum arquivo seja enviado, a aplicação gera automaticamente uma base sintética realista de 18 meses com sazonalidade e ticket variável.
- **Mapeador Inteligente de Colunas**: Permite subir qualquer arquivo CSV ou Excel e indicar quais colunas correspondem ao ID do Cliente, Data da Transação, ID da Transação e Valor Total.
- **KPIs C-Level**: Receita Total, Clientes Únicos, Ticket Médio Geral e o indicador em destaque de **🚨 Receita em Risco**.
- **Gráficos Interativos em Plotly**:
  - *Treemap* de representatividade financeira por cluster.
  - *Dispersão 3D* com rotação livre (Recência x Frequência x Valor Monetário).
  - *Matriz 5x5* de densidade de clientes.
- **Exportação Operacional para CRM**: Filtro por cluster e download imediato de planilha CSV formatada para Excel (`utf-8-sig`) pronta para envio aos executivos de vendas.
