/**
 * PORTFÓLIO DE DADOS & BI - MAIN.JS
 * Interações, Animações de Métricas, Chart.js e Modal de Estudo de Caso
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileMenu();
  initMetricCounters();
  initProjectFilters();
  initCaseStudyModal();
  initInteractiveChart();
  initCohortAnalysis();
  initRfmAnalysis();
  initContactActions();
});

/* ==========================================================================
   1. MENU MOBILE
   ========================================================================== */
function initMobileMenu() {
  const menuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  const menuLinks = document.querySelectorAll('.mobile-nav-link');

  if (!menuBtn || !mobileMenu) return;

  menuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });

  menuLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.add('hidden');
    });
  });
}

/* ==========================================================================
   2. CONTADORES ANIMADOS DE IMPACTO (INTERSECTION OBSERVER)
   ========================================================================== */
function initMetricCounters() {
  const metricCards = document.querySelectorAll('[data-target-value]');
  if (!metricCards.length) return;

  let hasAnimated = false;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !hasAnimated) {
        hasAnimated = true;
        metricCards.forEach(card => {
          const target = parseFloat(card.getAttribute('data-target-value'));
          const prefix = card.getAttribute('data-prefix') || '';
          const suffix = card.getAttribute('data-suffix') || '';
          const isDecimal = card.getAttribute('data-decimal') === 'true';
          const duration = 1800; // ms
          const startTime = performance.now();

          function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const easeOut = 1 - Math.pow(1 - progress, 3);
            const current = target * easeOut;

            const formatted = isDecimal 
              ? current.toFixed(1) 
              : Math.floor(current);

            card.textContent = `${prefix}${formatted}${suffix}`;

            if (progress < 1) {
              requestAnimationFrame(updateNumber);
            } else {
              card.textContent = `${prefix}${target}${suffix}`;
            }
          }

          requestAnimationFrame(updateNumber);
        });
      }
    });
  }, { threshold: 0.3 });

  const metricsSection = document.getElementById('metricas');
  if (metricsSection) {
    observer.observe(metricsSection);
  }
}

/* ==========================================================================
   3. FILTROS DA SEÇÃO DE PROJETOS
   ========================================================================== */
function initProjectFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  if (!filterBtns.length || !projectCards.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterValue === 'all' || category === filterValue) {
          card.style.display = 'block';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 50);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(15px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 250);
        }
      });
    });
  });
}

/* ==========================================================================
   4. MODAL DETALHADO DE ESTUDOS DE CASO
   ========================================================================== */
const caseStudiesData = {
  logistica: {
    title: "Otimização de Custos de Frete & Auditoria Contratual",
    category: "Otimização de Custos & Finanças",
    impact: "Redução de 40% em sobretaxas e recuperação de R$ 1.2M",
    tags: ["SQL Avançado", "Looker (LookML)", "Python (Pandas)", "BigQuery", "Data Governance"],
    problem: `
      A operação lidava com mais de 80.000 entregas mensais distribuídas entre 14 transportadoras parceiras. 
      A ausência de auditoria sistemática fazia com que taxas acessórias indevidas (diárias extras, taxa de reentrega injustificada e cubagem divergente) 
      fossem faturadas sem contestação, gerando estouro orçamentário superior a 15% ao mês.
    `,
    solution: `
      1. <strong>Pipeline de Conciliação em Python:</strong> Script automatizado para extração, validação e cruzamento de XMLs de NF-e e CT-e com as tabelas contratuais vigentes.<br>
      2. <strong>Modelagem de Auditoria em BigQuery / SQL:</strong> Uso de Window Functions e CTEs para recalcular o peso cúbico e a tarifa contratual exata para cada frete emitido.<br>
      3. <strong>Cockpit Operacional no Looker:</strong> Criação de dashboard de divergências em tempo real para o time de Logística aprovar faturas ou gerar cartas de contestação automáticas.
    `,
    codeSnippet: `-- Exemplo de detecção de divergência de cubagem e sobretaxa
WITH CalculoContratual AS (
    SELECT 
        cte.numero_cte,
        cte.transportadora_id,
        cte.valor_faturado,
        -- Cálculo da cubagem contratada vs peso real
        GREATEST(cte.peso_real, cte.volume_m3 * tab.fator_cubagem) AS peso_tarifado_esperado,
        (tab.tarifa_base + (GREATEST(cte.peso_real, cte.volume_m3 * tab.fator_cubagem) * tab.preco_kg)) AS valor_devido
    FROM bronze_fretes.ctes cte
    INNER JOIN silver_contratos.tabelas_vigentes tab
        ON cte.transportadora_id = tab.transportadora_id
        AND cte.data_emissao BETWEEN tab.vigencia_inicio AND tab.vigencia_fim
)
SELECT 
    numero_cte,
    transportadora_id,
    valor_faturado,
    valor_devido,
    (valor_faturado - valor_devido) AS divergencia_cobrada
FROM CalculoContratual
WHERE (valor_faturado - valor_devido) > 15.00
ORDER BY divergencia_cobrada DESC;`,
    results: [
      "40% de redução nas sobretaxas acessórias não contratuais logo no primeiro trimestre.",
      "R$ 1.200.000 recuperados em glosas e notas contestadas em auditoria retroativa de 12 meses.",
      "Ciclo de conferência de faturas reduzido de 12 dias úteis para aprovação em menos de 2 horas."
    ]
  },
  bi: {
    title: "Camada Semântica Corporativa & Cockpit Executivo",
    category: "Business Intelligence & Governança",
    impact: "Unificação de 14 KPIs críticos e suporte a 120+ decisores",
    tags: ["Power BI", "dbt", "Modelagem Dimensional", "DAX", "PostgreSQL"],
    problem: `
      Divergência crônica entre os relatórios da área Comercial e da Controladoria. 
      Vendas reportava receita com base em pedidos emitidos, enquanto Finanças reportava com base em faturamento líquido e baixas contábeis. 
      As reuniões de diretoria perdiam tempo discutindo a veracidade dos dados ao invés de estratégias de expansão.
    `,
    solution: `
      1. <strong>Modelagem Dimensional (Kimball):</strong> Construção de Fatos e Dimensões compartilhadas (Conformed Dimensions) com dbt garantindo granularidade atômica.<br>
      2. <strong>Camada Semântica Centralizada:</strong> Criação de métricas corporativas imutáveis no dbt / Power BI (MRR, Margem de Contribuição, Churn e LTV).<br>
      3. <strong>Governança e RLS:</strong> Implementação de Row-Level Security por região e unidade de negócio com painéis de navegação intuitiva para C-Level e gerentes.
    `,
    codeSnippet: `// Medida DAX Corporativa com Padronização Contábil
Margem_Contribuicao_Liquida := 
VAR ReceitaLiquida = 
    CALCULATE(
        SUM(faturamento[valor_liquido]),
        dim_status_nf[aprovada] = TRUE()
    )
VAR CustoVariavel = 
    CALCULATE(
        SUM(custos[custo_produto_vendido]) + SUM(fretes[frete_rateado]),
        dim_status_nf[aprovada] = TRUE()
    )
RETURN
    DIVIDE(ReceitaLiquida - CustoVariavel, ReceitaLiquida, 0)`,
    results: [
      "Fonte única da verdade adotada por 100% da diretoria e mais de 120 gestores operacionais.",
      "Fechamento do reporte executivo mensal acelerado de 5 dias úteis para visualização em D-0.",
      "Identificação de 3 linhas de produtos com margem líquida negativa, possibilitando reajuste imediato de precificação."
    ]
  },
  automacao: {
    title: "Orquestração de Pipelines e Alertas Proativos",
    category: "Engenharia de Dados & Automação",
    impact: "18 horas/semana economizadas e detecção de incidentes em < 5 min",
    tags: ["n8n", "Python", "Webhooks", "PostgreSQL", "Slack API"],
    problem: `
      A equipe de analistas gastava entre 3 e 4 horas diárias baixando arquivos CSV de múltiplos portais de parceiros, 
      fazendo joins manuais no Excel e conferindo estoque. Anomalias como pedidos retidos ou falhas de sincronização 
      só eram percebidas quando clientes abriam chamados de reclamação.
    `,
    solution: `
      1. <strong>Orquestração com n8n:</strong> Workflows agendados consumindo APIs REST, realizando validações de integridade e gravando em banco analítico.<br>
      2. <strong>Script de Análise Estatística em Python:</strong> Cálculo em tempo real de Z-score no volume de vendas e lead time de entrega para detectar quebras de padrão.<br>
      3. <strong>Bots de Notificação Contextual:</strong> Envio de alertas inteligentes com botões de ação direta nos canais do Slack e Teams para os times de suporte e logística.
    `,
    codeSnippet: `# Script Python para detecção de anomalias no pipeline de pedidos
import pandas as pd
import numpy as np

def detectar_anomalia_volume(df_pedidos):
    # Calcula média móvel de 7 dias e desvio padrão por categoria
    df_stats = df_pedidos.groupby('categoria')['volume_hora'].agg(['mean', 'std']).reset_index()
    df_merged = df_pedidos.merge(df_stats, on='categoria')
    
    # Detecção com limite de Z-Score > 2.5 (anomalia estatística)
    df_merged['z_score'] = (df_merged['volume_hora'] - df_merged['mean']) / df_merged['std'].replace(0, 1)
    anomalias = df_merged[df_merged['z_score'].abs() > 2.5]
    
    return anomalias[['timestamp', 'categoria', 'volume_hora', 'z_score']]`,
    results: [
      "100% dos processos diários de ingestão de relatórios automatizados sem intervenção humana.",
      "Economia direta de mais de 18 horas semanais de trabalho repetitivo do time analítico.",
      "Redução no tempo de identificação de falhas sistêmicas de 14 horas para menos de 5 minutos."
    ]
  },
  cohort: {
    title: "Modelagem de Cohort, Retenção & Prevenção de Churn",
    category: "Analytics de Vendas & SaaS",
    impact: "Aumento de 18 p.p. na retenção e R$ 640k em ARR recuperado",
    tags: ["SQL Window Functions", "dbt", "Python (Cohort Heatmap)", "Power BI", "LTV/CAC Modeling"],
    problem: `
      A empresa apresentava forte volume de novos clientes no topo de funil, porém sofria com uma evasão silenciosa de 28% da base nos primeiros 60 dias pós-conversão (Early Churn).
      Essa perda precoce drenava o Life Time Value (LTV), elevava o período de Payback do CAC para mais de 14 meses e gerava desalinhamento entre Marketing, Vendas e Customer Success.
    `,
    solution: `
      1. <strong>Identificação da Safra Inicial (First-Touch Cohort):</strong> Criação de pipeline no Data Warehouse mapeando a data da 1ª transação/assinatura de cada cliente via SQL.<br>
      2. <strong>Cálculo Dinâmico de Retenção Longitudinal:</strong> Matriz temporal calculando a diferença em meses (M0 a M6+) entre a safra de origem e compras subsequentes.<br>
      3. <strong>Detecção de Padrões de Churn (Survival Curve):</strong> Descoberta analítica de que clientes sem ativação de 2 recursos-chave até o 14º dia apresentavam risco 3.8x maior de evasão.<br>
      4. <strong>Automação de Ações Proativas:</strong> Disparo de gatilhos automáticos para CS ao detectar declínio de consumo no período crítico antes da renovação.
    `,
    codeSnippet: `-- Pipeline SQL para Matriz de Cohort e Retenção Mensal
WITH ClientesSafra AS (
    -- Define a data de aquisição/safra de cada cliente
    SELECT 
        cliente_id,
        DATE_TRUNC(MIN(data_compra), MONTH) AS safra_mes
    FROM gold_vendas.fator_transacoes
    WHERE status_pagamento = 'CONCLUIDO'
    GROUP BY cliente_id
),
AtividadeMensal AS (
    -- Identifica os meses em que o cliente realizou compras ativas
    SELECT DISTINCT
        t.cliente_id,
        s.safra_mes,
        DATE_TRUNC(t.data_compra, MONTH) AS mes_atividade,
        DATE_DIFF(DATE_TRUNC(t.data_compra, MONTH), s.safra_mes, MONTH) AS periodo_m
    FROM gold_vendas.fator_transacoes t
    INNER JOIN ClientesSafra s ON t.cliente_id = s.cliente_id
    WHERE t.status_pagamento = 'CONCLUIDO'
),
TamanhoSafras AS (
    -- Contagem do tamanho inicial de cada coorte (M0)
    SELECT 
        safra_mes, 
        COUNT(DISTINCT cliente_id) AS total_clientes_m0
    FROM ClientesSafra
    GROUP BY safra_mes
)
-- Matriz Final de Retenção Percentual por Safra e Período (M0 a M6)
SELECT 
    a.safra_mes,
    s.total_clientes_m0,
    a.periodo_m,
    COUNT(DISTINCT a.cliente_id) AS clientes_ativos,
    ROUND(COUNT(DISTINCT a.cliente_id) * 100.0 / s.total_clientes_m0, 1) AS taxa_retencao_pct,
    ROUND(100.0 - (COUNT(DISTINCT a.cliente_id) * 100.0 / s.total_clientes_m0), 1) AS taxa_churn_pct
FROM AtividadeMensal a
INNER JOIN TamanhoSafras s ON a.safra_mes = s.safra_mes
GROUP BY a.safra_mes, s.total_clientes_m0, a.periodo_m
ORDER BY a.safra_mes, a.periodo_m;`,
    results: [
      "Identificação do gap crítico de engajamento entre os dias D14 e D28, permitindo redesenhar o onboarding de clientes.",
      "Aumento de 18 pontos percentuais na taxa de retenção de M3 (de 58% para 76%) nas safras que utilizaram a nova jornada orientada a dados.",
      "Redução consolidada de 25% no Churn involuntário com automação de alertas proativos de risco.",
      "Preservação de aproximadamente R$ 640.000 em ARR anualizado na carteira de clientes."
    ]
  },
  rfm: {
    title: "Segmentação RFM & Prevenção de Churn em Vendas",
    category: "CRM Analytics, Retenção & Machine Intelligence",
    impact: "Mapeamento de R$ 485k em risco e +35% de retenção reativada",
    tags: ["Python (Pandas/NumPy)", "Streamlit", "Plotly", "Quantis RFM (qcut)", "CRM Playbooks", "LTV Modeling"],
    problem: `
      A empresa operava com uma base ativa de mais de 800 clientes recorrentes, porém adotava uma abordagem comercial uniforme para toda a carteira. 
      Clientes de altíssimo volume histórico (grandes contas) entravam em inatividade sem alertas prévios, enquanto clientes novos recebiam a mesma régua de comunicação 
      que compradores esporádicos. Essa homogeneidade analítica gerava perda silenciosa de clientes VIPs e desgaste da equipe comercial com leads de baixo retorno.
    `,
    solution: `
      1. <strong>Motor Analítico RFM em Python:</strong> Engenharia de features para cálculo de Recência (dias desde a última transação), Frequência (pedidos únicos) e Valor Monetário (soma faturada).<br>
      2. <strong>Pontuação por Quantis com Desempate:</strong> Aplicação rigorosa de <code>pd.qcut</code> com <code>rank(method='first')</code> para eliminar distorções de empates em clientes de 1 única compra, ranqueando de 1 a 5 cada dimensão com rigor estatístico.<br>
      3. <strong>Matriz de 11 Clusters Estratégicos:</strong> Classificação determinística em clusters de negócio (Campeões, Leais, Potenciais Leais, Novos, Promissores, Precisam de Atenção, Quase Hibernando, Em Risco, Não Podemos Perder, Hibernando, Perdidos).<br>
      4. <strong>Cockpit Executivo em Streamlit & Exportação CRM:</strong> Interface com Treemap financeiro, dispersão 2D/3D interativa, visualização de receita em risco e download imediato de listas operacionais em CSV (<code>utf-8-sig</code>) com playbooks personalizados.
    `,
    codeSnippet: `# Motor de Cálculo e Pontuação por Quantis RFM
import pandas as pd

def calculate_rfm(df, ref_date):
    # 1. Agregação dos pilares por cliente
    rfm = df.groupby('id_cliente').agg({
        'data_transacao': lambda x: (ref_date - x.max()).days,
        'id_transacao': 'nunique',
        'valor_total': 'sum'
    }).rename(columns={'data_transacao': 'Recencia', 'id_transacao': 'Frequencia', 'valor_total': 'Valor'})

    # 2. Atribuição de Scores de 1 a 5 via Quantis com desempate
    rfm['R_Score'] = pd.qcut(rfm['Recencia'].rank(method='first'), q=5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm['F_Score'] = pd.qcut(rfm['Frequencia'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Valor'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

    # 3. Código composto e classificação determinística dos 11 clusters
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    rfm['Segmento'] = rfm.apply(lambda r: assign_segment(r['R_Score'], r['F_Score'], r['M_Score']), axis=1)
    
    return rfm`,
    results: [
      "Identificação imediata de R$ 485.200 (24.8% da receita global) concentrados nos clusters críticos 'Não Podemos Perder' e 'Em Risco'.",
      "Priorização de 100% dos contatos dos gerentes de contas, focando exclusivamente nas contas de maior risco e alto LTV.",
      "Aumento de 35% na taxa de sucesso de reativação após o envio de ofertas direcionadas por canal prioritário (WhatsApp Concierge e Ligação Executiva).",
      "Redução do tempo de diagnóstico da carteira de 3 dias no Excel para execução automatizada em menos de 10 segundos no Streamlit."
    ]
  }
};

function initCaseStudyModal() {
  const modalBackdrop = document.getElementById('caseStudyModal');
  const modalBody = document.getElementById('modalBody');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const openModalBtns = document.querySelectorAll('[data-case-study]');

  if (!modalBackdrop || !modalBody) return;

  function openModal(caseKey) {
    const data = caseStudiesData[caseKey];
    if (!data) return;

    modalBody.innerHTML = `
      <div class="border-b border-neutral-800 pb-5 mb-6">
        <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
          <span class="text-xs font-mono px-2.5 py-1 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">${data.category}</span>
          <span class="text-xs font-semibold text-emerald-400 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> ${data.impact}
          </span>
        </div>
        <h3 class="text-2xl font-bold text-white mb-3">${data.title}</h3>
        <div class="flex flex-wrap gap-2">
          ${data.tags.map(tag => `<span class="tech-badge text-xs">${tag}</span>`).join('')}
        </div>
      </div>

      <div class="space-y-6 text-sm text-neutral-300">
        <div>
          <h4 class="text-xs font-mono uppercase tracking-wider text-neutral-400 mb-2 flex items-center gap-2">
            <svg class="w-4 h-4 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
            O Desafio de Negócio
          </h4>
          <p class="leading-relaxed bg-neutral-900/60 p-4 rounded-lg border border-neutral-800/80">${data.problem}</p>
        </div>

        <div>
          <h4 class="text-xs font-mono uppercase tracking-wider text-neutral-400 mb-2 flex items-center gap-2">
            <svg class="w-4 h-4 text-sky-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"/></svg>
            Arquitetura & Metodologia
          </h4>
          <div class="leading-relaxed bg-neutral-900/60 p-4 rounded-lg border border-neutral-800/80 space-y-2">${data.solution}</div>
        </div>

        <div>
          <h4 class="text-xs font-mono uppercase tracking-wider text-neutral-400 mb-2 flex items-center gap-2">
            <svg class="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            Destaque Técnico de Implementação
          </h4>
          <pre class="code-block"><code>${data.codeSnippet}</code></pre>
        </div>

        <div>
          <h4 class="text-xs font-mono uppercase tracking-wider text-neutral-400 mb-2 flex items-center gap-2">
            <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            Resultados Mensuráveis & ROI
          </h4>
          <ul class="space-y-2.5 bg-neutral-900/60 p-4 rounded-lg border border-neutral-800/80">
            ${data.results.map(res => `
              <li class="flex items-start gap-2.5">
                <span class="text-emerald-400 mt-0.5">✔</span>
                <span>${res}</span>
              </li>
            `).join('')}
          </ul>
        </div>
      </div>
    `;

    modalBackdrop.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modalBackdrop.classList.remove('open');
    document.body.style.overflow = '';
  }

  openModalBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const caseKey = btn.getAttribute('data-case-study');
      openModal(caseKey);
    });
  });

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', closeModal);
  }

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop.classList.contains('open')) {
      closeModal();
    }
  });
}

/* ==========================================================================
   5. MINI DEMONSTRAÇÃO INTERATIVA COM CHART.JS
   ========================================================================== */
function initInteractiveChart() {
  const canvas = document.getElementById('demoChart');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let currentView = 'cost'; // 'cost' ou 'volume'
  let currentPeriod = '6m'; // '6m' ou '12m'

  // Dados para 6 meses
  const data6m = {
    months: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    // Custo em R$ Milhares
    costActual: [320, 310, 295, 220, 190, 185], // Queda após o mês de Março (implementação)
    costTarget: [280, 280, 280, 250, 220, 200],
    // Volume em milhares e SLA em %
    volume: [45, 48, 52, 60, 68, 75],
    sla: [94.2, 94.8, 96.0, 98.9, 99.4, 99.6]
  };

  // Dados para 12 meses
  const data12m = {
    months: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
    costActual: [320, 310, 295, 220, 190, 185, 180, 175, 172, 170, 168, 165],
    costTarget: [280, 280, 280, 250, 220, 200, 190, 185, 180, 175, 170, 170],
    volume: [45, 48, 52, 60, 68, 75, 78, 82, 85, 89, 92, 95],
    sla: [94.2, 94.8, 96.0, 98.9, 99.4, 99.6, 99.7, 99.8, 99.8, 99.9, 99.9, 99.9]
  };

  // Configuração inicial do gráfico
  let chartInstance = new Chart(ctx, getChartConfig('cost', '6m'));

  function getChartConfig(view, period) {
    const d = period === '6m' ? data6m : data12m;

    if (view === 'cost') {
      return {
        type: 'line',
        data: {
          labels: d.months,
          datasets: [
            {
              label: 'Custo Real Faturado (R$ mil)',
              data: d.costActual,
              borderColor: '#38bdf8',
              backgroundColor: 'rgba(56, 189, 248, 0.12)',
              fill: true,
              tension: 0.35,
              borderWidth: 3,
              pointBackgroundColor: '#38bdf8',
              pointRadius: 4,
              pointHoverRadius: 7
            },
            {
              label: 'Orçamento / Meta (R$ mil)',
              data: d.costTarget,
              borderColor: '#818cf8',
              borderDash: [5, 5],
              backgroundColor: 'transparent',
              fill: false,
              tension: 0.2,
              borderWidth: 2,
              pointBackgroundColor: '#818cf8',
              pointRadius: 3
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            legend: {
              labels: {
                color: '#94a3b8',
                font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 }
              }
            },
            tooltip: {
              backgroundColor: '#0f121d',
              titleColor: '#f8fafc',
              bodyColor: '#94a3b8',
              borderColor: 'rgba(255, 255, 255, 0.1)',
              borderWidth: 1,
              padding: 12,
              callbacks: {
                label: function(context) {
                  return ` ${context.dataset.label}: R$ ${context.parsed.y} mil`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#64748b' }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: {
                color: '#64748b',
                callback: value => `R$ ${value}k`
              }
            }
          }
        }
      };
    } else {
      // Visão Volume & SLA
      return {
        type: 'bar',
        data: {
          labels: d.months,
          datasets: [
            {
              type: 'bar',
              label: 'Volume de Entregas (milhares)',
              data: d.volume,
              backgroundColor: 'rgba(99, 102, 241, 0.4)',
              borderColor: '#6366f1',
              borderWidth: 1,
              borderRadius: 6,
              yAxisID: 'y'
            },
            {
              type: 'line',
              label: 'SLA Operacional (%)',
              data: d.sla,
              borderColor: '#10b981',
              backgroundColor: 'transparent',
              borderWidth: 3,
              pointBackgroundColor: '#10b981',
              pointRadius: 4,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false
          },
          plugins: {
            legend: {
              labels: {
                color: '#94a3b8',
                font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 }
              }
            },
            tooltip: {
              backgroundColor: '#0f121d',
              titleColor: '#f8fafc',
              bodyColor: '#94a3b8',
              borderColor: 'rgba(255, 255, 255, 0.1)',
              borderWidth: 1,
              padding: 12
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#64748b' }
            },
            y: {
              type: 'linear',
              position: 'left',
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: '#64748b' }
            },
            y1: {
              type: 'linear',
              position: 'right',
              min: 90,
              max: 100,
              grid: { drawOnChartArea: false },
              ticks: {
                color: '#10b981',
                callback: value => `${value}%`
              }
            }
          }
        }
      };
    }
  }

  // Controles de alternância de visão
  const btnCost = document.getElementById('chartViewCost');
  const btnVolume = document.getElementById('chartViewVolume');
  const btnCohort = document.getElementById('chartViewCohort');
  const btnRfm = document.getElementById('chartViewRfm');
  const chartContainer = document.getElementById('chartContainer');
  const cohortContainer = document.getElementById('cohortContainer');
  const rfmContainer = document.getElementById('rfmContainer');
  const periodFiltersWrapper = document.getElementById('periodFiltersWrapper');
  const periodBtns = document.querySelectorAll('[data-period]');
  const chipKpi1 = document.getElementById('chipKpi1');
  const chipKpi2 = document.getElementById('chipKpi2');
  const footerPipeline = document.getElementById('demoFooterPipeline');
  const footerNote = document.getElementById('demoFooterNote');
  const cardTestRfmBtn = document.getElementById('cardTestRfmBtn');

  function updateKpiChips() {
    if (currentView === 'cost') {
      if (chipKpi1) chipKpi1.innerHTML = 'Economia Acumulada: <strong class="text-emerald-400 font-mono">R$ 840.000</strong>';
      if (chipKpi2) chipKpi2.innerHTML = 'Redução Médio Ponderada: <strong class="text-sky-400 font-mono">-41.2%</strong>';
      if (footerPipeline) footerPipeline.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400"></span><span>Pipeline: Modelagem SQL + Conciliação em Python + Validação Looker</span>';
      if (footerNote) footerNote.textContent = 'Ponto de virada implementado no Mês de Março (Q1)';
    } else if (currentView === 'volume') {
      if (chipKpi1) chipKpi1.innerHTML = 'Volume Processado: <strong class="text-indigo-400 font-mono">820k entregas</strong>';
      if (chipKpi2) chipKpi2.innerHTML = 'Acurácia de SLA: <strong class="text-emerald-400 font-mono">99.8%</strong>';
      if (footerPipeline) footerPipeline.innerHTML = '<span class="w-2 h-2 rounded-full bg-indigo-400"></span><span>Pipeline: Kafka Stream + Ingestão PostgreSQL + Alertas Proativos</span>';
      if (footerNote) footerNote.textContent = 'SLA mantido consistentemente acima da meta operacional de 98.5%';
    } else if (currentView === 'cohort') {
      if (chipKpi1) chipKpi1.innerHTML = 'Retenção M3 Média: <strong class="text-cyan-400 font-mono">76.8%</strong>';
      if (chipKpi2) chipKpi2.innerHTML = 'Queda Churn Precoce: <strong class="text-emerald-400 font-mono">-47.2% (Jan vs Jun)</strong>';
      if (footerPipeline) footerPipeline.innerHTML = '<span class="w-2 h-2 rounded-full bg-cyan-400"></span><span>Pipeline: First-Touch SQL + Modelagem Dimensional dbt + Matriz Heatmap</span>';
      if (footerNote) footerNote.textContent = 'Nova jornada de onboarding ativada em Março/24 refletindo nas safras seguintes';
    } else if (currentView === 'rfm') {
      if (chipKpi1) chipKpi1.innerHTML = 'Receita em Risco: <strong class="text-rose-400 font-mono">R$ 485.200 (24.8%)</strong>';
      if (chipKpi2) chipKpi2.innerHTML = 'Segmentação: <strong class="text-emerald-400 font-mono">11 Clusters (100%)</strong>';
      if (footerPipeline) footerPipeline.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-400"></span><span>Pipeline: Engine Python + Quantis RFM (qcut) + Streamlit App</span>';
      if (footerNote) footerNote.textContent = 'Priorização automatizada de contas e ações táticas para CRM e Vendas';
    }
  }

  function setButtonInactive(btn) {
    if (!btn) return;
    btn.classList.remove(
      'bg-sky-500/20', 'text-sky-300', 'border-sky-500/40',
      'bg-cyan-500/20', 'text-cyan-300', 'border-cyan-500/40',
      'bg-emerald-500/20', 'text-emerald-300', 'border-emerald-500/40'
    );
    btn.classList.add('text-neutral-400', 'border-transparent');
  }

  if (btnCost) {
    btnCost.addEventListener('click', () => {
      currentView = 'cost';
      btnCost.classList.add('bg-sky-500/20', 'text-sky-300', 'border-sky-500/40');
      btnCost.classList.remove('text-neutral-400', 'border-transparent');
      setButtonInactive(btnVolume);
      setButtonInactive(btnCohort);
      setButtonInactive(btnRfm);

      if (chartContainer) chartContainer.classList.remove('hidden');
      if (cohortContainer) cohortContainer.classList.add('hidden');
      if (rfmContainer) rfmContainer.classList.add('hidden');
      if (periodFiltersWrapper) periodFiltersWrapper.classList.remove('hidden');

      chartInstance.destroy();
      chartInstance = new Chart(ctx, getChartConfig(currentView, currentPeriod));
      updateKpiChips();
    });
  }

  if (btnVolume) {
    btnVolume.addEventListener('click', () => {
      currentView = 'volume';
      btnVolume.classList.add('bg-sky-500/20', 'text-sky-300', 'border-sky-500/40');
      btnVolume.classList.remove('text-neutral-400', 'border-transparent');
      setButtonInactive(btnCost);
      setButtonInactive(btnCohort);
      setButtonInactive(btnRfm);

      if (chartContainer) chartContainer.classList.remove('hidden');
      if (cohortContainer) cohortContainer.classList.add('hidden');
      if (rfmContainer) rfmContainer.classList.add('hidden');
      if (periodFiltersWrapper) periodFiltersWrapper.classList.remove('hidden');

      chartInstance.destroy();
      chartInstance = new Chart(ctx, getChartConfig(currentView, currentPeriod));
      updateKpiChips();
    });
  }

  if (btnCohort) {
    btnCohort.addEventListener('click', () => {
      currentView = 'cohort';
      btnCohort.classList.add('bg-cyan-500/20', 'text-cyan-300', 'border-cyan-500/40');
      btnCohort.classList.remove('text-neutral-400', 'border-transparent');
      setButtonInactive(btnCost);
      setButtonInactive(btnVolume);
      setButtonInactive(btnRfm);

      if (chartContainer) chartContainer.classList.add('hidden');
      if (cohortContainer) cohortContainer.classList.remove('hidden');
      if (rfmContainer) rfmContainer.classList.add('hidden');
      if (periodFiltersWrapper) periodFiltersWrapper.classList.add('hidden');

      updateKpiChips();
    });
  }

  if (btnRfm) {
    btnRfm.addEventListener('click', () => {
      currentView = 'rfm';
      btnRfm.classList.add('bg-emerald-500/20', 'text-emerald-300', 'border-emerald-500/40');
      btnRfm.classList.remove('text-neutral-400', 'border-transparent');
      setButtonInactive(btnCost);
      setButtonInactive(btnVolume);
      setButtonInactive(btnCohort);

      if (chartContainer) chartContainer.classList.add('hidden');
      if (cohortContainer) cohortContainer.classList.add('hidden');
      if (rfmContainer) rfmContainer.classList.remove('hidden');
      if (periodFiltersWrapper) periodFiltersWrapper.classList.add('hidden');

      updateKpiChips();
    });
  }

  if (cardTestRfmBtn) {
    cardTestRfmBtn.addEventListener('click', () => {
      if (btnRfm) btnRfm.click();
    });
  }

  periodBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      periodBtns.forEach(b => {
        b.classList.remove('bg-neutral-800', 'text-white');
        b.classList.add('text-neutral-400');
      });
      btn.classList.add('bg-neutral-800', 'text-white');
      btn.classList.remove('text-neutral-400');

      currentPeriod = btn.getAttribute('data-period');
      if (currentView !== 'cohort') {
        chartInstance.destroy();
        chartInstance = new Chart(ctx, getChartConfig(currentView, currentPeriod));
      }
    });
  });
}

/* ==========================================================================
   6. ANÁLISE DE COHORT & CHURN (HEATMAP INTERATIVO)
   ========================================================================== */
function initCohortAnalysis() {
  const tableBody = document.getElementById('cohortTableBody');
  const btnRetention = document.getElementById('cohortMetricRetention');
  const btnChurn = document.getElementById('cohortMetricChurn');
  const legendLow = document.getElementById('cohortLegendLow');
  const legendHigh = document.getElementById('cohortLegendHigh');
  const insightTitle = document.getElementById('cohortInsightTitle');
  const insightDesc = document.getElementById('cohortInsightDesc');
  const activeMetric = document.getElementById('cohortActiveMetric');

  if (!tableBody) return;

  let currentMetricMode = 'retention'; // 'retention' ou 'churn'

  const cohortData = [
    {
      safra: "Jan/24",
      novosClientes: 1250,
      receitaSafra: "R$ 185k",
      retencao: [100.0, 85.6, 78.4, 74.2, 71.8, 69.4, 68.2],
      churn:    [0.0,   14.4, 21.6, 25.8, 28.2, 30.6, 31.8],
      clientes: [1250, 1070, 980, 928, 898, 868, 853],
      receita:  ["R$ 185k", "R$ 158k", "R$ 145k", "R$ 137k", "R$ 133k", "R$ 128k", "R$ 126k"],
      destaque: "Safra Baseline inicial"
    },
    {
      safra: "Fev/24",
      novosClientes: 1420,
      receitaSafra: "R$ 210k",
      retencao: [100.0, 84.8, 77.9, 73.5, 70.9, 68.8, null],
      churn:    [0.0,   15.2, 22.1, 26.5, 29.1, 31.2, null],
      clientes: [1420, 1204, 1106, 1044, 1007, 977, null],
      receita:  ["R$ 210k", "R$ 178k", "R$ 164k", "R$ 154k", "R$ 149k", "R$ 144k", null],
      destaque: "Pico de churn inicial em M1"
    },
    {
      safra: "Mar/24",
      novosClientes: 1680,
      receitaSafra: "R$ 254k",
      retencao: [100.0, 88.2, 82.4, 78.9, 76.5, null, null],
      churn:    [0.0,   11.8, 17.6, 21.1, 23.5, null, null],
      clientes: [1680, 1482, 1384, 1326, 1285, null, null],
      receita:  ["R$ 254k", "R$ 224k", "R$ 209k", "R$ 200k", "R$ 194k", null, null],
      destaque: "Início do Onboarding Orientado a Dados (Inflexão)"
    },
    {
      safra: "Abr/24",
      novosClientes: 1850,
      receitaSafra: "R$ 280k",
      retencao: [100.0, 89.5, 84.1, 80.8, null, null, null],
      churn:    [0.0,   10.5, 15.9, 19.2, null, null, null],
      clientes: [1850, 1656, 1556, 1495, null, null, null],
      receita:  ["R$ 280k", "R$ 251k", "R$ 235k", "R$ 226k", null, null, null],
      destaque: "Gatilhos automáticos de CS ativos"
    },
    {
      safra: "Mai/24",
      novosClientes: 2100,
      receitaSafra: "R$ 318k",
      retencao: [100.0, 91.2, 86.7, null, null, null, null],
      churn:    [0.0,   8.8,  13.3, null, null, null, null],
      clientes: [2100, 1915, 1821, null, null, null, null],
      receita:  ["R$ 318k", "R$ 290k", "R$ 276k", null, null, null, null],
      destaque: "Melhor Safra Histórica (+22% LTV)"
    },
    {
      safra: "Jun/24",
      novosClientes: 2340,
      receitaSafra: "R$ 355k",
      retencao: [100.0, 92.4, null, null, null, null, null],
      churn:    [0.0,   7.6,  null, null, null, null, null],
      clientes: [2340, 2162, null, null, null, null, null],
      receita:  ["R$ 355k", "R$ 328k", null, null, null, null, null],
      destaque: "Retenção recorde de M1 (92.4%)"
    }
  ];

  function getHeatClass(val, mode) {
    if (val === null) return 'cohort-empty';
    if (mode === 'retention') {
      if (val >= 100) return 'ret-100';
      if (val >= 85) return 'ret-80';
      if (val >= 75) return 'ret-70';
      if (val >= 65) return 'ret-60';
      if (val >= 50) return 'ret-50';
      return 'ret-low';
    } else {
      if (val <= 5) return 'churn-0';
      if (val <= 12) return 'churn-15';
      if (val <= 20) return 'churn-25';
      if (val <= 28) return 'churn-35';
      return 'churn-45';
    }
  }

  function renderTable() {
    tableBody.innerHTML = '';

    cohortData.forEach(row => {
      const tr = document.createElement('tr');
      const values = currentMetricMode === 'retention' ? row.retencao : row.churn;

      let cellsHtml = `
        <td class="text-left font-semibold text-white whitespace-nowrap">
          ${row.safra}
          ${row.destaque.includes('Início') || row.destaque.includes('Melhor') ? '<span class="text-cyan-400 ml-1 text-xs" title="' + row.destaque + '">★</span>' : ''}
        </td>
        <td class="text-neutral-300 font-mono text-center">${row.novosClientes.toLocaleString('pt-BR')}</td>
        <td class="text-emerald-400 font-mono text-center">${row.receitaSafra}</td>
      `;

      for (let i = 0; i <= 6; i++) {
        const val = values[i];
        if (val !== null && val !== undefined) {
          const heatClass = getHeatClass(val, currentMetricMode);
          cellsHtml += `
            <td class="cohort-cell ${heatClass}" 
                data-safra="${row.safra}" 
                data-period="M${i}" 
                data-val="${val.toFixed(1)}%" 
                data-clients="${row.clientes[i] ? row.clientes[i].toLocaleString('pt-BR') : '-'}" 
                data-revenue="${row.receita[i] || '-'}"
                data-destaque="${row.destaque}">
              ${val.toFixed(1)}%
            </td>
          `;
        } else {
          cellsHtml += `<td class="cohort-empty">-</td>`;
        }
      }

      tr.innerHTML = cellsHtml;
      tableBody.appendChild(tr);
    });

    attachCellListeners();
  }

  function attachCellListeners() {
    const cells = document.querySelectorAll('.cohort-cell');
    cells.forEach(cell => {
      cell.addEventListener('mouseenter', () => {
        const safra = cell.getAttribute('data-safra');
        const period = cell.getAttribute('data-period');
        const val = cell.getAttribute('data-val');
        const clients = cell.getAttribute('data-clients');
        const revenue = cell.getAttribute('data-revenue');
        const destaque = cell.getAttribute('data-destaque');

        const modeLabel = currentMetricMode === 'retention' ? 'Taxa de Retenção' : 'Taxa de Churn';

        if (insightTitle) insightTitle.textContent = `Safra ${safra} • Período ${period} (${modeLabel})`;
        if (insightDesc) {
          insightDesc.innerHTML = `Clientes Ativos: <strong class="text-white font-mono">${clients}</strong> | Receita Retida: <strong class="text-emerald-400 font-mono">${revenue}</strong>${destaque ? ` | <span class="text-cyan-400">★ ${destaque}</span>` : ''}`;
        }
        if (activeMetric) {
          activeMetric.textContent = `${modeLabel}: ${val}`;
          activeMetric.className = currentMetricMode === 'retention' 
            ? 'font-mono text-emerald-400 text-sm font-bold sm:text-right' 
            : 'font-mono text-rose-400 text-sm font-bold sm:text-right';
        }
      });
    });
  }

  if (btnRetention && btnChurn) {
    btnRetention.addEventListener('click', () => {
      currentMetricMode = 'retention';
      btnRetention.classList.add('bg-emerald-500/20', 'text-emerald-300', 'border-emerald-500/40');
      btnRetention.classList.remove('text-neutral-400', 'border-transparent');
      btnChurn.classList.remove('bg-emerald-500/20', 'text-emerald-300', 'border-emerald-500/40', 'bg-rose-500/20', 'text-rose-300', 'border-rose-500/40');
      btnChurn.classList.add('text-neutral-400', 'border-transparent');

      if (legendLow) {
        legendLow.textContent = 'Menor (<50%)';
        legendLow.className = 'px-2 py-0.5 rounded bg-neutral-800 text-neutral-400';
      }
      if (legendHigh) {
        legendHigh.textContent = 'Maior (100%)';
        legendHigh.className = 'px-2 py-0.5 rounded bg-emerald-500/30 text-emerald-300 font-bold';
      }

      renderTable();
    });

    btnChurn.addEventListener('click', () => {
      currentMetricMode = 'churn';
      btnChurn.classList.add('bg-rose-500/20', 'text-rose-300', 'border-rose-500/40');
      btnChurn.classList.remove('text-neutral-400', 'border-transparent');
      btnRetention.classList.remove('bg-emerald-500/20', 'text-emerald-300', 'border-emerald-500/40');
      btnRetention.classList.add('text-neutral-400', 'border-transparent');

      if (legendLow) {
        legendLow.textContent = '0% Churn';
        legendLow.className = 'px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300';
      }
      if (legendHigh) {
        legendHigh.textContent = 'Alto Churn (>30%)';
        legendHigh.className = 'px-2 py-0.5 rounded bg-rose-500/30 text-rose-300 font-bold';
      }

      renderTable();
    });
  }

  // Render inicial da tabela
  renderTable();
}

/* ==========================================================================
   7. ANÁLISE DE SEGMENTAÇÃO RFM (COCKPIT INTERATIVO)
   ========================================================================== */
function initRfmAnalysis() {
  const matrixBody = document.getElementById('rfmMatrixBody');
  const clusterPills = document.getElementById('rfmClusterPills');
  const playbookCard = document.getElementById('rfmPlaybookCard');
  const copyCmdBtn = document.getElementById('copyStreamlitCmdBtn');

  if (!matrixBody || !playbookCard) return;

  // Dicionário com os 11 Clusters RFM
  const rfmClusters = {
    "Campeões": {
      cor: "#10B981",
      prioridade: "Alta",
      descricao: "Compraram muito recentemente, compram com alta frequência e possuem os maiores volumes de faturamento.",
      objetivo: "Fidelização máxima, retenção ativa e programas de evangelização da marca.",
      plano: [
        "Acesso antecipado a novos produtos e lançamentos VIP.",
        "Atendimento com Gerente de Contas dedicado (Key Account).",
        "Recompensas exclusivas por indicação de novos clientes corporativos.",
        "Não enviar cupons de desconto agressivos (eles já compram pelo valor)."
      ],
      canais: "WhatsApp Concierge, Contato Telefônico Executivo, E-mail VIP"
    },
    "Leais": {
      cor: "#3B82F6",
      prioridade: "Alta",
      descricao: "Compras consistentes, boa frequência e gastos acima da média da carteira.",
      objetivo: "Aumentar o Lifetime Value (LTV) através de cross-selling e up-selling.",
      plano: [
        "Apresentar produtos complementares de tíquete superior.",
        "Incentivar adesão a programas de benefícios com pontuação cumulativa.",
        "Solicitar depoimentos e cases de sucesso para prova social."
      ],
      canais: "E-mail Segmentado, WhatsApp Comercial, Notificações Proativas"
    },
    "Potenciais Clientes Leais": {
      cor: "#8B5CF6",
      prioridade: "Média-Alta",
      descricao: "Clientes recentes que já realizaram mais de 1 compra com engajamento promissor.",
      objetivo: "Transformar compradores recorrentes em clientes leais e defensores da marca.",
      plano: [
        "Enviar réguas de nutrição com casos de uso e melhores práticas.",
        "Ofertar incentivo na 3ª ou 4ª compra com validade curta (escassez).",
        "Convidar para webinars ou comunidade exclusiva de clientes."
      ],
      canais: "E-mail Educativo, WhatsApp Comercial, Remarketing de Catálogo"
    },
    "Novos Clientes": {
      cor: "#06B6D4",
      prioridade: "Média",
      descricao: "Compraram pela primeira vez muito recentemente. Alto potencial inicial.",
      objetivo: "Garantir sucesso no onboarding e induzir a segunda compra o mais rápido possível.",
      plano: [
        "E-mail de boas-vindas acolhedor e pesquisa rápida pós-primeira compra.",
        "Enviar tutorial passo a passo de aproveitamento do produto.",
        "Disponibilizar cupom de incentivo para a 2ª compra válido por 30 dias."
      ],
      canais: "E-mail de Onboarding, SMS/WhatsApp com Boas-Vindas"
    },
    "Promissores": {
      cor: "#14B8A6",
      prioridade: "Média",
      descricao: "Compradores recentes de primeira compra com tíquete moderado.",
      objetivo: "Criar vínculo e percepção de valor para estimular a primeira recompra.",
      plano: [
        "Campanhas baseadas na categoria do primeiro item comprado.",
        "Apresentar avaliações de outros compradores em categorias similares.",
        "Ofertas de produtos 'best-sellers' com condições especiais de frete."
      ],
      canais: "E-mail Marketing, Remarketing de Catálogo"
    },
    "Precisam de Atenção": {
      cor: "#F59E0B",
      prioridade: "Alta",
      descricao: "Recência e frequência moderadas. Risco iminente de esfriamento se não estimulados.",
      objetivo: "Reativar o hábito de compra antes da entrada na zona de inatividade.",
      plano: [
        "Campanhas de incentivo com tempo limitado (ofertas 'flash' de 48h).",
        "Ofertar combos ou kits de reposição com desconto no pacote.",
        "Apresentar novidades do portfólio adicionadas desde a última compra."
      ],
      canais: "E-mail de Oportunidade, Remarketing Display, WhatsApp Comercial"
    },
    "Quase Hibernando": {
      cor: "#F97316",
      prioridade: "Média",
      descricao: "Baixa recência e pouca frequência. Clientes prestes a se tornarem inativos.",
      objetivo: "Evitar o churn definitivo com comunicação de reengajamento assertiva.",
      plano: [
        "Campanha 'Sentimos sua falta' com benefício direto e expressivo na volta.",
        "Apresentar produtos populares com condições facilitadas de pagamento.",
        "Questionar de forma breve se o produto anterior atendeu às expectativas."
      ],
      canais: "E-mail de Reativação, Anúncios Segmentados de Custom Audience"
    },
    "Não Podemos Perder": {
      cor: "#DC2626",
      prioridade: "Crítica",
      descricao: "Clientes históricos de altíssima frequência e valor que deixaram de comprar há muito tempo.",
      objetivo: "Reconquista urgente e investigação de atrito/insatisfação. Risco financeiro crítico.",
      plano: [
        "Contato direto e pessoal de SDR/Gerente de Contas via ligação executiva.",
        "Investigar se houve insatisfação com suporte, qualidade ou migração para concorrente.",
        "Ofertar plano de renovação sob medida com condições especiais irrecusáveis.",
        "Envolver liderança comercial para resgate do relacionamento institucional."
      ],
      canais: "Ligação Telefônica Direta, Reunião Presencial/Online, WhatsApp Executivo"
    },
    "Em Risco": {
      cor: "#EF4444",
      prioridade: "Crítica",
      descricao: "Histórico sólido de compras que deixaram de comprar no período recente.",
      objetivo: "Interromper o processo de churn e recapturar a atenção do cliente.",
      plano: [
        "Pesquisa de satisfação para entender motivos de afastamento.",
        "Cupons substanciais de reativação para a volta.",
        "Apresentar lançamentos e melhorias recentes que o cliente não conheceu."
      ],
      canais: "E-mail de Reconquista, WhatsApp de Relacionamento, Retargeting"
    },
    "Hibernando": {
      cor: "#64748B",
      prioridade: "Baixa",
      descricao: "Frequência muito baixa e última compra realizada há muitos meses.",
      objetivo: "Reativação de baixo custo ou higienização da base de contatos.",
      plano: [
        "Campanhas de queima de estoque ou promoções sazonais agressivas (ex: Black Friday).",
        "Opção simples de opt-out para manter reputação de entregabilidade do domínio."
      ],
      canais: "E-mail Marketing Automatizado de Baixo Custo"
    },
    "Perdidos": {
      cor: "#475569",
      prioridade: "Baixa",
      descricao: "Compraram uma única vez no passado distante e nunca mais retornaram.",
      objetivo: "Última tentativa de contato de baixo custo ou desativação de envios.",
      plano: [
        "Disparo de régua única 'Sentimos sua falta: cupom especial de retorno'.",
        "Se não houver clique após 30 dias, pausar envios de marketing para cortar custos."
      ],
      canais: "E-mail de Despedida / Limpeza de Base"
    }
  };

  // Matriz 5x5: [R5, R4, R3, R2, R1] cruzando com [F1, F2, F3, F4, F5]
  const rfmMatrixData = [
    {
      rowScore: 5,
      rowLabel: "R5 (Mais Recente)",
      cells: [
        { f: 1, cluster: "Novos Clientes", clients: 68, rev: "R$ 42.100", cls: "rfm-bg-novos" },
        { f: 2, cluster: "Potenciais Clientes Leais", clients: 54, rev: "R$ 68.300", cls: "rfm-bg-potenciais" },
        { f: 3, cluster: "Leais", clients: 38, rev: "R$ 94.200", cls: "rfm-bg-leais" },
        { f: 4, cluster: "Campeões", clients: 42, rev: "R$ 158.400", cls: "rfm-bg-campeoes" },
        { f: 5, cluster: "Campeões", clients: 46, rev: "R$ 214.600", cls: "rfm-bg-campeoes" }
      ]
    },
    {
      rowScore: 4,
      rowLabel: "R4 (Recente)",
      cells: [
        { f: 1, cluster: "Novos Clientes", clients: 58, rev: "R$ 36.500", cls: "rfm-bg-novos" },
        { f: 2, cluster: "Potenciais Clientes Leais", clients: 48, rev: "R$ 59.800", cls: "rfm-bg-potenciais" },
        { f: 3, cluster: "Leais", clients: 36, rev: "R$ 88.700", cls: "rfm-bg-leais" },
        { f: 4, cluster: "Campeões", clients: 34, rev: "R$ 126.900", cls: "rfm-bg-campeoes" },
        { f: 5, cluster: "Campeões", clients: 30, rev: "R$ 142.100", cls: "rfm-bg-campeoes" }
      ]
    },
    {
      rowScore: 3,
      rowLabel: "R3 (Médio)",
      cells: [
        { f: 1, cluster: "Promissores", clients: 52, rev: "R$ 31.400", cls: "rfm-bg-promissores" },
        { f: 2, cluster: "Precisam de Atenção", clients: 44, rev: "R$ 52.600", cls: "rfm-bg-atencao" },
        { f: 3, cluster: "Precisam de Atenção", clients: 32, rev: "R$ 64.100", cls: "rfm-bg-atencao" },
        { f: 4, cluster: "Leais", clients: 26, rev: "R$ 78.500", cls: "rfm-bg-leais" },
        { f: 5, cluster: "Leais", clients: 22, rev: "R$ 96.300", cls: "rfm-bg-leais" }
      ]
    },
    {
      rowScore: 2,
      rowLabel: "R2 (Em Risco)",
      cells: [
        { f: 1, cluster: "Quase Hibernando", clients: 48, rev: "R$ 27.200", cls: "rfm-bg-quase-dormindo" },
        { f: 2, cluster: "Quase Hibernando", clients: 38, rev: "R$ 41.800", cls: "rfm-bg-quase-dormindo" },
        { f: 3, cluster: "Em Risco", clients: 28, rev: "R$ 62.400", cls: "rfm-bg-em-risco" },
        { f: 4, cluster: "Não Podemos Perder", clients: 24, rev: "R$ 98.700", cls: "rfm-bg-nao-perder" },
        { f: 5, cluster: "Não Podemos Perder", clients: 20, rev: "R$ 124.500", cls: "rfm-bg-nao-perder" }
      ]
    },
    {
      rowScore: 1,
      rowLabel: "R1 (Mais Antigo)",
      cells: [
        { f: 1, cluster: "Perdidos", clients: 64, rev: "R$ 29.800", cls: "rfm-bg-perdidos" },
        { f: 2, cluster: "Hibernando", clients: 42, rev: "R$ 38.200", cls: "rfm-bg-hibernando" },
        { f: 3, cluster: "Em Risco", clients: 30, rev: "R$ 61.200", cls: "rfm-bg-em-risco" },
        { f: 4, cluster: "Não Podemos Perder", clients: 22, rev: "R$ 84.600", cls: "rfm-bg-nao-perder" },
        { f: 5, cluster: "Não Podemos Perder", clients: 18, rev: "R$ 115.000", cls: "rfm-bg-nao-perder" }
      ]
    }
  ];

  let selectedClusterName = "Não Podemos Perder"; // Destaque inicial no cluster crítico de receita em risco

  // 1. Renderiza a Matriz 5x5
  function renderMatrix() {
    matrixBody.innerHTML = '';

    rfmMatrixData.forEach(row => {
      const tr = document.createElement('tr');
      let trHtml = `<td class="text-left font-semibold text-neutral-400 whitespace-nowrap pr-2">${row.rowLabel}</td>`;

      row.cells.forEach(cell => {
        const isClusterMatch = cell.cluster === selectedClusterName;
        trHtml += `
          <td class="rfm-cell ${cell.cls} ${isClusterMatch ? 'active-cell' : ''}" 
              data-cluster="${cell.cluster}" 
              data-r="R${row.rowScore}" 
              data-f="F${cell.f}" 
              data-clients="${cell.clients}" 
              data-rev="${cell.rev}">
            <div class="font-bold leading-tight">${cell.cluster}</div>
            <div class="text-[10px] opacity-80 mt-0.5">${cell.clients} cli • ${cell.rev}</div>
          </td>
        `;
      });

      tr.innerHTML = trHtml;
      matrixBody.appendChild(tr);
    });

    // Adiciona listener de clique nas células da matriz
    const cells = matrixBody.querySelectorAll('.rfm-cell');
    cells.forEach(cell => {
      cell.addEventListener('click', () => {
        const cluster = cell.getAttribute('data-cluster');
        selectCluster(cluster);
      });
    });
  }

  // 2. Renderiza as Pílulas dos Clusters
  function renderPills() {
    if (!clusterPills) return;
    clusterPills.innerHTML = '';

    Object.keys(rfmClusters).forEach(name => {
      const btn = document.createElement('button');
      btn.className = `rfm-pill-btn ${name === selectedClusterName ? 'active' : ''}`;
      btn.textContent = name;
      btn.addEventListener('click', () => {
        selectCluster(name);
      });
      clusterPills.appendChild(btn);
    });
  }

  // 3. Renderiza o Card de Playbook Tático
  function renderPlaybook() {
    const meta = rfmClusters[selectedClusterName];
    if (!meta) return;

    const prioColor = 
      meta.prioridade === 'Crítica' ? 'text-rose-400 bg-rose-500/10 border-rose-500/30' :
      meta.prioridade === 'Alta' ? 'text-amber-400 bg-amber-500/10 border-amber-500/30' :
      'text-sky-400 bg-sky-500/10 border-sky-500/30';

    playbookCard.style.borderLeftColor = meta.cor;
    playbookCard.style.borderLeftWidth = '4px';

    playbookCard.innerHTML = `
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-neutral-800">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full" style="background-color: ${meta.cor};"></span>
          <h4 class="text-sm font-bold text-white uppercase tracking-wider font-mono">
            Playbook Comercial: ${selectedClusterName}
          </h4>
        </div>
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold border uppercase self-start sm:self-auto ${prioColor}">
          Prioridade: ${meta.prioridade}
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
        <div class="space-y-2">
          <div>
            <span class="text-neutral-400 font-mono text-[10px] uppercase block">Perfil & Diagnóstico:</span>
            <p class="text-neutral-300 leading-relaxed">${meta.descricao}</p>
          </div>
          <div>
            <span class="text-neutral-400 font-mono text-[10px] uppercase block">Objetivo de Negócio:</span>
            <p class="text-emerald-400 font-medium">${meta.objetivo}</p>
          </div>
          <div>
            <span class="text-neutral-400 font-mono text-[10px] uppercase block">Canais Recomendados:</span>
            <code class="px-2 py-1 rounded bg-neutral-800 text-sky-300 font-mono text-[11px] block mt-1">${meta.canais}</code>
          </div>
        </div>

        <div class="space-y-1.5">
          <span class="text-neutral-400 font-mono text-[10px] uppercase block">Plano de Ação Tático para CRM/Vendas:</span>
          <ul class="space-y-1.5 bg-neutral-950/60 p-3 rounded-xl border border-neutral-800/80">
            ${meta.plano.map(item => `
              <li class="flex items-start gap-2 text-neutral-300">
                <span class="text-sky-400 mt-0.5 font-bold">›</span>
                <span>${item}</span>
              </li>
            `).join('')}
          </ul>
        </div>
      </div>
    `;
  }

  function selectCluster(name) {
    selectedClusterName = name;
    renderMatrix();
    renderPills();
    renderPlaybook();
  }

  // Ação de copiar comando Streamlit
  if (copyCmdBtn) {
    copyCmdBtn.addEventListener('click', () => {
      const cmd = "streamlit run Projetos/01_Cockpit_RFM_Analytics/app.py";
      navigator.clipboard.writeText(cmd).then(() => {
        if (typeof window.showToast === 'function') {
          window.showToast("Comando copiado: " + cmd, "success");
        } else {
          alert("Comando copiado: " + cmd);
        }
      }).catch(() => {
        if (typeof window.showToast === 'function') {
          window.showToast("Execute no terminal: " + cmd, "info");
        }
      });
    });
  }

  // Inicialização do cockpit RFM
  selectCluster(selectedClusterName);
}

/* ==========================================================================
   8. CONTATO, CÓPIA DE E-MAIL E ENVIO FORMSPREE
   ========================================================================== */
function initContactActions() {
  const copyBtn = document.getElementById('copyEmailBtn');
  const toast = document.getElementById('toast');
  const toastMessage = document.getElementById('toastMessage');
  const toastIcon = document.getElementById('toastIcon');
  const emailAddress = "fernandoc.job@gmail.com";

  let toastTimeout = null;

  function showToast(msg, type = 'success') {
    if (!toast) return;
    if (toastMessage) toastMessage.textContent = msg;

    // Reset classes e adiciona estilo correspondente ao tipo
    toast.className = '';
    toast.classList.add('show');

    if (type === 'error') {
      toast.classList.add('toast-error');
      if (toastIcon) {
        toastIcon.className = 'w-5 h-5 text-rose-400 flex-shrink-0';
        toastIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />';
      }
    } else if (type === 'info') {
      toast.classList.add('toast-info');
      if (toastIcon) {
        toastIcon.className = 'w-5 h-5 text-sky-400 flex-shrink-0';
        toastIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />';
      }
    } else {
      toast.classList.add('toast-success');
      if (toastIcon) {
        toastIcon.className = 'w-5 h-5 text-emerald-400 flex-shrink-0';
        toastIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />';
      }
    }

    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      toast.classList.remove('show');
    }, 4000);
  }

  // Expor globalmente para uso pelo cockpit RFM
  window.showToast = showToast;

  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(emailAddress).then(() => {
        showToast('E-mail copiado para a área de transferência!', 'success');
      }).catch(() => {
        showToast(`E-mail: ${emailAddress}`, 'info');
      });
    });
  }

  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      const nameInput = document.getElementById('contactName');
      const emailInput = document.getElementById('contactEmail');
      const messageInput = document.getElementById('contactMessage');
      const submitBtn = contactForm.querySelector('button[type="submit"]');
      const originalBtnHtml = submitBtn ? submitBtn.innerHTML : '';

      if (!nameInput.value.trim() || !emailInput.value.trim() || !messageInput.value.trim()) {
        e.preventDefault();
        showToast('Por favor, preencha todos os campos obrigatórios.', 'error');
        return;
      }

      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(emailInput.value.trim())) {
        e.preventDefault();
        showToast('Por favor, insira um e-mail com formato válido.', 'error');
        return;
      }

      // Se executado diretamente via arquivo local (protocolo file:///),
      // navegadores bloqueiam requisições fetch por política de CORS (Origin: null).
      // Nesse caso, permitimos o envio nativo do formulário HTML que funciona 100% no Formspree!
      if (window.location.protocol === 'file:') {
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.innerHTML = '<span>Enviando formulário...</span>';
        }
        return true;
      }

      // Em ambiente com servidor HTTP/HTTPS (GitHub Pages, Vercel, localhost, etc.), usa AJAX:
      e.preventDefault();

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
          <svg class="animate-spin h-4 w-4 text-white inline-block mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Enviando mensagem...</span>
        `;
      }

      try {
        const formData = new FormData(contactForm);
        const response = await fetch(contactForm.action, {
          method: 'POST',
          body: formData,
          headers: {
            'Accept': 'application/json'
          }
        });

        if (response.ok) {
          showToast('Mensagem enviada com sucesso! Responderei em breve.', 'success');
          contactForm.reset();
        } else {
          const data = await response.json().catch(() => ({}));
          if (data && data.errors && data.errors.length) {
            const errorText = data.errors.map(err => err.message).join(', ');
            showToast(`Formspree: ${errorText}`, 'error');
          } else {
            showToast('Conectando via envio direto...', 'info');
            setTimeout(() => {
              contactForm.submit();
            }, 600);
          }
        }
      } catch (error) {
        console.warn('Erro na requisição AJAX ao Formspree, acionando fallback nativo:', error);
        showToast('Enviando via conexão segura de formulário...', 'info');
        setTimeout(() => {
          contactForm.submit();
        }, 600);
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnHtml;
        }
      }
    });
  }
}
