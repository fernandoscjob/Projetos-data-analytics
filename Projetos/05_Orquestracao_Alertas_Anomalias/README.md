# ⚙️ Orquestração de Pipelines e Alertas Proativos de Anomalias

![Status](https://img.shields.io/badge/Status-Produção-emerald?style=for-the-badge)
![n8n](https://img.shields.io/badge/Orchestration-n8n_Workflows-EA4B71?style=for-the-badge&logo=n8n)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql)
![Slack](https://img.shields.io/badge/Alerts-Slack_API-4A154B?style=for-the-badge&logo=slack)

Pipeline automatizado de orquestração de dados e monitoramento em tempo real com **n8n** e **Python**, capaz de identificar quebras bruscas de padrão (Z-Score > 2.5) em streams de vendas e disparar alertas acionáveis no Slack/Teams antes que clientes sejam impactados.

---

## 💼 Contexto de Negócio & Desafio

A equipe de analistas gastava entre 3 e 4 horas por dia baixando planilhas de múltiplos portais, fazendo cruzamentos manuais no Excel e validando estoques.
- Anomalias críticas, como quedas de gateway de pagamento ou atrasos logísticos, só eram descobertas após dezenas de reclamações de clientes no suporte.

**Resultados Mensurados:**
- **100% dos relatórios diários automatizados**, sem qualquer intervenção humana manual.
- **Economia direta de 18 horas semanais** da equipe analítica.
- Tempo médio de detecção de incidentes sistêmicos reduzido de 14 horas para **menos de 5 minutos**.

---

## 🧠 Arquitetura de Detecção Estatística

1. **Trigger n8n a cada 15 minutos:** Consulta incremental de transações recentes no PostgreSQL.
2. **Cálculo de Desvio Estatístico (Z-Score):**
   $$Z = \frac{X_t - \mu_{\text{hist}}}{\sigma_{\text{hist}}}$$
   - Se $|Z| \ge 2.5$, o registro é classificado como anomalia grave (queda de conversão ou pico anormal de tráfego).
3. **Disparo de Payload Contextual:** Montagem de cards interativos via Slack Block Kit com link direto para o painel de resolução.

---

## 📁 Estrutura de Arquivos

```
05_Orquestracao_Alertas_Anomalias/
├── anomaly_detector.py           # Motor estatístico Python de cálculo de Z-score e payload
├── n8n_workflow_alertas.json     # Workflow n8n exportado pronto para importação
├── requirements.txt              # Dependências (pandas, numpy, requests)
└── README.md                     # Documentação técnica do projeto
```

---

## 🚀 Como Executar Localmente

```bash
cd Projetos/05_Orquestracao_Alertas_Anomalias
python anomaly_detector.py
```
O script simulará 72 horas de telemetria de pedidos com uma anomalia forçada de gateway e imprimirá o alerta gerado e o payload do webhook.
