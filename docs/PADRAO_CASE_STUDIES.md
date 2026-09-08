# 🏛️ Padrão Oficial de Storytelling e Engenharia para Cases de Dados

Este documento estabelece a diretriz oficial para a documentação e apresentação de todos os cases de portfólio de **Fernando Cavalcante**. Ele é inspirado no renomado case de **Detecção de Fraude do Walmart**, unindo o rigor científico da metodologia **CRISP-DM** com o foco executivo em **ROI, finanças e tomada de decisão ágil**.

---

## 📋 Prompt Base para Geração de Novos Cases

Ao desenvolver um novo projeto, utilize a seguinte estrutura para documentar as informações brutas:

```markdown
### INFORMAÇÕES BRUTAS DO PROJETO:
- **Nome do Projeto:** [Nome formal e impactante do projeto]
- **Empresa/Contexto:** [Segmento de mercado, porte e desafio do setor]
- **O Problema de Negócio:** [Dores operacionais, ineficiências financeiras ou pontos cegos de tomada de decisão]
- **Dados Utilizados:** [Origem das fontes, formato, volume transacional e período histórico]
- **Abordagem Técnica Aplicada:** [Stack tecnológica: SQL Avançado, Python, dbt, modelagem dimensional, DAX, etc.]
- **Resultados de Negócio Obtidos:** [Métricas de ROI, economia financeira em R$, horas salvas e ganhos percentuais]
- **Principais Insights Descobertos:** [Padrões ocultos, gargalos operacionais e oportunidades mapeadas]
```

---

## 🏗️ Estrutura Canônica do Estudo de Caso (6 Seções Obrigatórias)

Todo case de portfólio (tanto na documentação `README.md` quanto no modal interativo do site) deve conter obrigatoriamente as 6 seções abaixo:

```markdown
# [Nome do Projeto]: [Subtítulo de Impacto Executivo]

### 🚀 1. TLDR (Too Long; Didn't Read) - Resumo Executivo
*Painel visual rápido de destaques para prender a atenção imediata do gestor:*
- **Objetivo do Projeto:** [Definição em 1 frase clara do problema resolvido]
- **Métricas Principais de Performance:** [Precisão do modelo, acurácia, confiabilidade ou volumetria processada]
- **Retorno Financeiro / Eficiência Gerada:** [ROI em R$ recuperados/economizados ou horas semanais poupadas]
- **Tempo de Execução / Resposta:** [Redução do tempo de resposta de dias/semanas para tempo real (D-0)]

---

### 💼 2. O Problema de Negócio (Business Understanding)
*Contextualização aprofundada da dor corporativa antes da implementação:*
- **Cenário Pré-Projeto:** Como a empresa operava antes da solução?
- **Custo da Inação:** Qual era a perda financeira silenciosa, desgaste de equipe ou risco regulatório/contratual?
- **Alinhamento Estratégico:** Por que a diretoria priorizou a resolução dessa dor?

---

### 🔬 3. Metodologia Científica e Técnica (CRISP-DM)
*Demonstração do processo científico e escolhas de engenharia estruturadas:*
- **Entendimento e Avaliação de Dados (Data Understanding):** 
  - Mapeamento das fontes de dados, granularidade e volume.
  - Análise Exploratória (EDA): identificação de valores nulos, duplicidades, assimetrias e outliers.
- **Preparação e Engenharia de Dados (Data Preparation):**
  - Pipelines de ingestão e transformação (ETL/ELT).
  - Arquitetura de modelagem dimensional (Star Schema / Fatos e Dimensões Conformes).
- **Modelagem Analítica (Modeling):**
  - Implementação matemática/estatística (medidas DAX robustas, quantis estatísticos ou algoritmos de Machine Learning).
  - *Snippet de código real com as regras de negócio centrais.*
- **Avaliação e Garantia de Qualidade (QA / Evaluation):**
  - Testes de integridade referencial, reconciliação financeira contra o ERP contábil e homologação com os usuários-chave.

---

### 📈 4. Resultados e Insights Gerados
*Descobertas quantitativas e qualitativas obtidas através da análise aprofundada:*
- **Diagnóstico Oculto:** O que os dados revelaram que a intuição corporativa não enxergava?
- **Ações Imediatas Desencadeadas:** Como as áreas de negócio agiram com base nas evidências?
- **Impacto Consolidado:** Tabela ou métricas comparativas (Antes vs. Depois).

---

### 🛠️ 5. Plano de Implementação, Governança e Próximos Passos
*Demonstração de maturidade sênior sobre a sustentabilidade da solução na rotina corporativa:*
- **Estratégia de Deploy & Segurança:** Agendamentos automáticos, controle de acesso (Row-Level Security - RLS) e contingência.
- **Matriz de Adoção (Quem Usa e Como):** 
  - Cargos e equipes usuárias (Ex.: C-Level, Gerentes de Contas, Analistas de Operações).
  - Como a rotina diária/semanal desses profissionais mudou (eliminação de planilhas paralelas).
- **Próximas Recomendações:** Melhorias incrementais sugeridas (automações adicionais, modelos preditivos ou integrações via API).

---

### 📊 6. Design do Dashboard de Suporte e Perguntas-Chave
*Arquitetura de visualização e decisões ágeis proporcionadas pelo painel:*
- **Audiência Específica:** Quem são os decisores primários e secundários do painel?
- **Perguntas de Negócio Respondidas em Menos de 5 Segundos:**
  1. *[Pergunta de Negócio 1]* -> *[Métrica visual que responde]*
  2. *[Pergunta de Negócio 2]* -> *[Métrica visual que responde]*
  3. *[Pergunta de Negócio 3]* -> *[Métrica visual que responde]*
- **Princípios de UX/UI Aplicados:** Hierarquia visual, redução da carga cognitiva e caminhos rápidos para exportação de planos de ação.
```

---

## 🎯 Regras de Ouro
1. **Nunca omita os números:** Sempre declare valores financeiros (R$), volumes de registros e ganhos percentuais com exatidão matemática.
2. **Conecte técnica a dinheiro:** Não diga apenas que usou `pd.qcut` ou `Window Functions`; explique que isso evitou distorções estatísticas que fariam a empresa perder R$ 485k em clientes VIPs.
3. **Pense na rotina do usuário:** Um projeto só termina quando a equipe operacional abandona o processo antigo e adota a nova rotina orientada a dados.
