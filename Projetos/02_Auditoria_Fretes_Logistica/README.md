# 🚚 Auditoria Contratual de Fretes & Otimização de Custos de Transporte

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![SQL](https://img.shields.io/badge/SQL-BigQuery_•_PostgreSQL-00758F?style=for-the-badge&logo=postgresql)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Looker](https://img.shields.io/badge/BI-Looker_(LookML)-4285F4?style=for-the-badge&logo=googlecloud)

Pipeline analítico de engenharia e auditoria de dados para conciliação automatizada de faturas de frete (CT-e) contra tabelas contratuais vigentes de transportadoras, identificação de cobranças indevidas (glosas) e otimização logística.

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
├── auditoria_fretes.py       # Motor Python de simulação, conciliação e geração de KPIs
├── queries_auditoria.sql     # Pipeline analítico em SQL (BigQuery/Postgres) com CTEs
├── requirements.txt          # Dependências mínimas (pandas, numpy)
└── README.md                 # Documentação técnica do projeto
```

---

## 🚀 Como Executar Localmente

```bash
cd Projetos/02_Auditoria_Fretes_Logistica
python auditoria_fretes.py
```
O script gerará uma amostra estocástica de 500 CT-es, aplicará as regras contratuais e imprimirá o resumo consolidado de valores recuperáveis por transportadora.
