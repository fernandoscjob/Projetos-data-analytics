/**
 * PORTFÓLIO DE DADOS & BI - DECK-VIEWER.JS
 * Visualizador Executivo Interativo em Tela Cheia (Executive Deck Mode 16:9)
 * Compatível com o Portfólio Principal e todos os Cockpits / Dashboards Analíticos
 * Desenvolvido por Fernando Cavalcante - Analista de Dados & Especialista em BI
 */

(function () {
  'use strict';

  // 1. Injetar Estilos do Visualizador se não existirem
  function ensureDeckStyles() {
    if (document.getElementById('deck-viewer-styles')) return;
    const style = document.createElement('style');
    style.id = 'deck-viewer-styles';
    style.textContent = `
      #deckViewerModal {
        transition: opacity 0.25s ease, visibility 0.25s ease;
      }
      #deckViewerModal.active {
        display: flex !important;
      }
      .deck-dot {
        width: 8px;
        height: 8px;
        border-radius: 9999px;
        background: rgba(255, 255, 255, 0.2);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: pointer;
      }
      .deck-dot:hover {
        background: rgba(255, 255, 255, 0.5);
      }
      .deck-dot.active {
        width: 24px;
        background: #38bdf8;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.5);
      }
      @keyframes deckSlideFadeIn {
        from {
          opacity: 0;
          transform: translateY(6px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
      .deck-slide-animated {
        animation: deckSlideFadeIn 0.25s ease-out forwards;
      }
      .btn-primary {
        background-color: #38bdf8;
        color: #020617;
        font-weight: 700;
        border-radius: 0.75rem;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      }
      .btn-primary:hover {
        background-color: #7dd3fc;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
      }
      .btn-secondary {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.12);
        color: #f8fafc;
        font-weight: 600;
        border-radius: 0.75rem;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
      }
      .btn-secondary:hover {
        background-color: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.25);
        color: #ffffff;
      }
      .tech-badge {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: #cbd5e1;
        font-family: 'JetBrains Mono', monospace;
        border-radius: 0.5rem;
      }
    `;
    document.head.appendChild(style);
  }

  // 2. Injetar Markup do Modal se não existir no DOM
  function ensureDeckModal() {
    let modal = document.getElementById('deckViewerModal');
    if (modal) return modal;

    modal = document.createElement('div');
    modal.id = 'deckViewerModal';
    modal.className = 'fixed inset-0 z-[100] hidden bg-black/95 backdrop-blur-xl flex flex-col items-center justify-center p-4 sm:p-8';
    modal.innerHTML = `
      <!-- Barra de Controle Superior -->
      <div class="w-full max-w-6xl flex items-center justify-between pb-4 text-xs font-mono text-neutral-400 border-b border-neutral-800">
        <div class="flex items-center gap-3">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span id="deckCaseTitle" class="text-white font-bold tracking-wider">APRESENTAÇÃO EXECUTIVA</span>
        </div>
        <div class="flex items-center gap-4">
          <span id="deckProgress">Slide 1 de 4</span>
          <button id="closeDeckBtn" class="p-1.5 rounded-lg bg-neutral-900 text-neutral-300 hover:text-white hover:bg-neutral-800 transition-colors" title="Fechar (ESC)">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Stage do Slide (Proporção 16:9 com Glassmorphism) -->
      <div class="w-full max-w-6xl aspect-[16/9] max-h-[80vh] my-auto relative rounded-3xl overflow-hidden glass-panel border border-neutral-800 p-6 sm:p-10 lg:p-12 flex flex-col justify-between shadow-2xl bg-neutral-950/80">
        <div id="deckSlideContent" class="h-full flex flex-col justify-between">
          <!-- Injetado dinamicamente via JavaScript -->
        </div>

        <!-- Navegação Inferior -->
        <div class="flex items-center justify-between pt-5 border-t border-neutral-800/80 mt-auto">
          <button id="prevSlideBtn" class="btn-secondary text-xs !py-2 !px-4 flex items-center gap-2">
            <span>← Anterior</span>
          </button>
          <div class="flex items-center gap-2" id="deckDots">
            <!-- Indicadores pontilhados gerados via JS -->
          </div>
          <button id="nextSlideBtn" class="btn-primary text-xs !py-2 !px-4 flex items-center gap-2">
            <span>Próximo →</span>
          </button>
        </div>
      </div>
    `;
    document.body.appendChild(modal);
    return modal;
  }

  const DECKS_DATA = {
    logistica: {
      title: '02. Auditoria Contratual de Fretes & Otimização de Custos',
      category: 'LOGÍSTICA & FINANÇAS • SUPPLY CHAIN',
      slides: [
        {
          tag: 'TESE DE NEGÓCIO & KPIS',
          headline: 'Auditoria Automatizada de Faturas e Fretes em Escala',
          subtext: 'Reconciliação algorítmica contínua entre CTEs faturados por transportadoras parceiras e tabelas vigentes, eliminando sobretaxas indevidas e recuperando capital em D-0.',
          type: 'kpis',
          kpis: [
            { label: 'Economia Obtida', value: '-40%', desc: 'Redução drástica em cobranças de taxas indevidas', colorClass: 'text-emerald-400' },
            { label: 'Recuperação Ativa', value: 'R$ 1.2M', desc: 'Valores glosados e contestados com êxito', colorClass: 'text-sky-400' },
            { label: 'Auditoria de CTEs', value: '100%', desc: 'Varredura automática contra 5% anterior por amostragem', colorClass: 'text-cyan-400' },
            { label: 'Parceiros Auditados', value: '14', desc: 'Transportadoras integradas na esteira analítica', colorClass: 'text-amber-400' }
          ]
        },
        {
          tag: 'RAIO-X DO PROBLEMA',
          headline: 'Vazamento Financeiro Invisível no Faturamento de Transportes',
          subtext: 'Antes da modelagem, a checagem manual por amostragem permitia a aprovação silenciosa de sobretaxas acessórias abusivas e cálculos volumétricos distorcidos.',
          type: 'pains',
          pains: [
            { icon: '⚖️', title: 'Cubagem Artificialmente Inflada', desc: 'Diferença sistemática de 18% no cálculo volumétrico (fator M3) faturado sem qualquer validação com dimensões cadastradas no ERP.', impact: 'R$ 380k / ano' },
            { icon: '🚫', title: 'Taxas Acessórias Fantasmas', desc: 'Cobrança não autorizada de estadias, reentregas e taxas de conferência sem comprovantes assinados ou geotags digitais.', impact: 'R$ 520k / ano' },
            { icon: '⏳', title: 'Gargalo Operacional Humano', desc: 'Equipe de Contas a Pagar gastava 4 dias por quinzena tentando conferir PDFs manualmente, liberando pagamentos sob pressão de prazo.', impact: '95% faturas cegas' }
          ]
        },
        {
          tag: 'ARQUITETURA & ENGENHARIA',
          headline: 'Pipeline de Conciliação em Python, SQL & Motor de Glosas',
          subtext: 'Automação de ponta a ponta: extração de dados fiscais (CTEs/XMLs), cruzamento com regras de cubagem e geração de laudos formais de contestação.',
          type: 'architecture',
          badges: ['Python 3.11', 'SQL Window Functions', 'Streamlit', 'Plotly Express', 'BigQuery / PostgreSQL', 'EDI Proceda'],
          phases: [
            { phase: 'ETL & Ingestão', title: 'Parsing de XMLs & Faturas', desc: 'Extração estruturada de chaves de acesso, pesos, distâncias e valores cobrados em lote.', codeSnippet: 'parse_cte_xml(files) -> DataFrame' },
            { phase: 'Motor de Regras', title: 'Cálculo de Tarifa Contratual', desc: 'Aplicação matricial da tabela negociada com tolerância estrita de R$ 0,05 por conhecimento.', codeSnippet: 'calc_tarifa_teorica(dist, peso_cubado)' },
            { phase: 'Automação Contábil', title: 'Emissão de Cartas de Glosa', desc: 'Geração de relatórios com evidências anexadas para desconto direto no Contas a Pagar.', codeSnippet: 'export_cartas_glosa_batch(transportadora)' }
          ]
        },
        {
          tag: 'IMPACTO & RECOMENDAÇÕES',
          headline: 'Retorno sobre Investimento Consolidado & Próximos Passos',
          subtext: 'Geração de valor financeiro imediato somada a um roadmap estruturado para blindagem logística e compras estratégicas.',
          type: 'roadmap',
          roadmap: [
            { horizon: '30 DIAS', timing: 'Curto Prazo', action: 'Bloqueio Preventivo no ERP', detail: 'Integração direta com o módulo de Contas a Pagar para travar faturas com divergência superior a 2%.', expectedRoi: 'Zero faturas pagas indevidamente', borderClass: 'border-sky-500', textClass: 'text-sky-400' },
            { horizon: '90 DIAS', timing: 'Médio Prazo', action: 'Repactuação de Tabela de Frete', detail: 'Renegociação de tarifas e cubagem com as transportadoras que apresentaram maior índice histórico de glosas.', expectedRoi: 'Redução adicional de 8% na base', borderClass: 'border-indigo-500', textClass: 'text-indigo-400' },
            { horizon: '180 DIAS', timing: 'Longo Prazo', action: 'TMS Inteligente Preditivo', detail: 'Simulador de menor custo total de rota antes da expedição, combinando prazo de entrega e SLA histórico.', expectedRoi: 'Eficiência de malha nacional', borderClass: 'border-emerald-500', textClass: 'text-emerald-400' }
          ]
        }
      ]
    },

    cohort: {
      title: '03. Modelagem de Cohort, Retenção & Prevenção de Churn',
      category: 'SAAS & VENDAS • CUSTOMER SUCCESS ANALYTICS',
      slides: [
        {
          tag: 'TESE DE NEGÓCIO & KPIS',
          headline: 'Elevação do LTV e Blindagem da Base Recorrente',
          subtext: 'Análise longitudinal do comportamento de safras de clientes para detectar o ponto exato de evasão e acionar estratégias prescritivas de engajamento.',
          type: 'kpis',
          kpis: [
            { label: 'Retenção em D90', value: '+18 p.p.', desc: 'Aumento de 52% para 70% na sobrevivência da safra', colorClass: 'text-emerald-400' },
            { label: 'Redução de Churn', value: '-25%', desc: 'Queda na taxa mensal de evasão involuntária', colorClass: 'text-cyan-400' },
            { label: 'ARR Preservado', value: 'R$ 640k', desc: 'Receita anual recorrente protegida contra cancelamento', colorClass: 'text-sky-400' },
            { label: 'Eficiência de CAC', value: '2.8x', desc: 'Relação LTV/CAC expandida em virtude da retenção', colorClass: 'text-amber-400' }
          ]
        },
        {
          tag: 'RAIO-X DO PROBLEMA',
          headline: 'Queda Prematura de Uso nos Primeiros 60 Dias de Ciclo',
          subtext: 'A visualização tradicional de churn agregado mascara a rápida degradação das safras recentes durante a fase de onboarding.',
          type: 'pains',
          pains: [
            { icon: '📉', title: 'Abandono Precoce no Onboarding', desc: '28% dos novos usuários deixavam de acessar a plataforma após 15 dias sem alcançar o "Aha Moment" de ativação.', impact: 'Perda de 1 em cada 3 clientes' },
            { icon: '🎭', title: 'Miopia de Métricas Agregadas', desc: 'Apresentar apenas o Churn Global (3.2%) escondia que as safras recentes perdiam o dobro de usuários das safras antigas.', impact: 'Atraso na tomada de decisão' },
            { icon: '🔔', title: 'Intervenção Tardia de Suporte', desc: 'O time de Customer Success só era notificado quando o cliente solicitava o cancelamento formal ou rescisão de contrato.', impact: 'Taxa de reversão menor que 8%' }
          ]
        },
        {
          tag: 'ARQUITETURA & ENGENHARIA',
          headline: 'Engenharia de Dados com SQL Window Functions & Matriz Cohort',
          subtext: 'Modelagem dimensional temporal calculando o índice de coorte de cada usuário e renderizando matrizes de calor interativas.',
          type: 'architecture',
          badges: ['SQL Window Functions', 'Python Cohort Matrix', 'dbt Core', 'Power BI / DAX', 'Heatmaps Interativos'],
          phases: [
            { phase: 'Definição de Safra', title: 'Timestamp da 1ª Transação', desc: 'Particionamento dos usuários pelo mês da primeira compra utilizando Window Functions.', codeSnippet: 'MIN(data_compra) OVER (PARTITION BY cliente_id)' },
            { phase: 'Cálculo de Defasagem', title: 'Cohort Index Normalizado', desc: 'Cálculo vetorial dos meses decorridos entre a safra inicial e transações subsequentes.', codeSnippet: '(ano_ev - ano_safra)*12 + (mes_ev - mes_safra)' },
            { phase: 'Visualização Tática', title: 'Gradiente de Retenção', desc: 'Renderização em tempo real de matrizes triangulares com coloração dinâmica condicional.', codeSnippet: 'renderCohortHeatmap(metric="retention")' }
          ]
        },
        {
          tag: 'IMPACTO & RECOMENDAÇÕES',
          headline: 'Retorno sobre Investimento Consolidado & Próximos Passos',
          subtext: 'Preservação comprovada de capital com intervenção proativa guiada pelo mapa de calor de retenção.',
          type: 'roadmap',
          roadmap: [
            { horizon: '30 DIAS', timing: 'Curto Prazo', action: 'Alertas Precoces no Slack', detail: 'Disparo de gatilho para o gestor da conta corporativa quando o cliente ficar sem logar por 7 dias em D30.', expectedRoi: 'Recuperação de 40% das contas em risco', borderClass: 'border-cyan-500', textClass: 'text-cyan-400' },
            { horizon: '90 DIAS', timing: 'Médio Prazo', action: 'Coortes Comportamentais por Feature', detail: 'Isolar safras com base no uso de funcionalidades específicas para guiar o roadmap do time de Produto.', expectedRoi: 'Aumento do engajamento em 30%', borderClass: 'border-indigo-500', textClass: 'text-indigo-400' },
            { horizon: '180 DIAS', timing: 'Longo Prazo', action: 'Modelo de Sobrevida Preditivo', detail: 'Implementação de regressão de Cox para estimar a probabilidade exata de sobrevivência individual.', expectedRoi: 'Previsibilidade orçamentária de ARR', borderClass: 'border-emerald-500', textClass: 'text-emerald-400' }
          ]
        }
      ]
    },

    bi: {
      title: '04. Camada Semântica & Cockpit Executivo de Planejamento',
      category: 'BI CORPORATIVO • DATA GOVERNANCE & KIMBALL',
      slides: [
        {
          tag: 'TESE DE NEGÓCIO & KPIS',
          headline: 'Fonte Única da Verdade (SSOT) para Lideranças Executivas',
          subtext: 'Substituição de planilhas departamentais desconexas por uma arquitetura dimensional em dbt e Power BI com governança estrita de regras de negócio.',
          type: 'kpis',
          kpis: [
            { label: 'Fechamento Mensal', value: 'D-0', desc: 'Disponibilidade imediata contra 5 dias de atraso anterior', colorClass: 'text-emerald-400' },
            { label: 'KPIs Homologados', value: '14', desc: 'Métricas corporativas padronizadas e auditadas', colorClass: 'text-indigo-400' },
            { label: 'Líderes Ativos', value: '120+', desc: 'Gestores e tomadores de decisão consultando o cockpit', colorClass: 'text-sky-400' },
            { label: 'Discrepâncias', value: '0%', desc: 'Alinhamento integral entre Comercial, Finanças e Operações', colorClass: 'text-cyan-400' }
          ]
        },
        {
          tag: 'RAIO-X DO PROBLEMA',
          headline: 'Guerra de Planilhas e Reuniões C-Level com Números Divergentes',
          subtext: 'A ausência de uma camada semântica unificada gerava discussões sobre a veracidade dos dados em vez de foco na tomada de decisão estratégica.',
          type: 'pains',
          pains: [
            { icon: '⚔️', title: 'Faturamento Divergente entre Áreas', desc: 'Comercial e Controladoria reportavam números com até 12% de diferença devido a regras distintas de cancelamentos e impostos.', impact: 'Desalinhamento executivo' },
            { icon: '📑', title: '18 Planilhas Paralelas de Excel', desc: 'Horas gastas atualizando arquivos pesados sujeitos a falhas de digitação, fórmulas quebradas e perda de histórico.', impact: '40h / mês de trabalho braçal' },
            { icon: '⚠️', title: 'Insegurança Regulatória e Auditoria', desc: 'Inexistência de linhagem de dados para justificar números contábeis aos auditores externos e conselho administrativo.', impact: 'Risco de conformidade fiscal' }
          ]
        },
        {
          tag: 'ARQUITETURA & ENGENHARIA',
          headline: 'Modelagem Kimball Star Schema, dbt & DAX Otimizado',
          subtext: 'Construção de tabelas Fatos e Dimensões Conformes, testes automáticos de dados e camada semântica com documentação viva.',
          type: 'architecture',
          badges: ['dbt Core', 'Modelagem Dimensional (Kimball)', 'Power BI', 'DAX Avançado', 'PostgreSQL / BigQuery', 'Git Versioning'],
          phases: [
            { phase: 'Modelagem Conceitual', title: 'Star Schema & Dimensões', desc: 'Fatos de Vendas e Faturamento conectadas a dimensões conformes de Tempo, Unidade e Cliente.', codeSnippet: 'fct_vendas -> dim_tempo, dim_cliente' },
            { phase: 'Transformação dbt', title: 'Regras de Negócio em SQL', desc: 'Testes de integridade referencial, singularidade e validação de regras fiscais automatizados.', codeSnippet: 'dbt test --models tag:faturamento' },
            { phase: 'Camada de Consumo', title: 'Power BI DAX & Governança', desc: 'Medidas rápidas com funções de inteligência temporal e políticas de acesso RLS por diretoria.', codeSnippet: 'YTD_Faturamento = TOTALYTD([Faturamento], dim_tempo)' }
          ]
        },
        {
          tag: 'IMPACTO & RECOMENDAÇÕES',
          headline: 'Retorno sobre Investimento Consolidado & Próximos Passos',
          subtext: 'Ganhos diretos de eficiência operacional e democratização do acesso a dados governados em toda a organização.',
          type: 'roadmap',
          roadmap: [
            { horizon: '30 DIAS', timing: 'Curto Prazo', action: 'Desativação das Planilhas Legadas', detail: 'Conclusão da migração das últimas planilhas financeiras com bloqueio de edição nos diretórios compartilhados.', expectedRoi: '100% de conformidade com a SSOT', borderClass: 'border-indigo-500', textClass: 'text-indigo-400' },
            { horizon: '90 DIAS', timing: 'Médio Prazo', action: 'Catálogo de Metadados Corporativo', detail: 'Disponibilização do dicionário interativo de métricas para todas as equipes de negócio.', expectedRoi: 'Autonomia analítica para 120 gestores', borderClass: 'border-sky-500', textClass: 'text-sky-400' },
            { horizon: '180 DIAS', timing: 'Longo Prazo', action: 'Camada GenAI Text-to-SQL', detail: 'Integração de assistente de inteligência artificial corporativa para responder dúvidas analíticas via chat.', expectedRoi: 'Consultas estratégicas em segundos', borderClass: 'border-emerald-500', textClass: 'text-emerald-400' }
          ]
        }
      ]
    },

    automacao: {
      title: '05. Orquestração de Pipelines e Alertas Proativos de Anomalias',
      category: 'ENGENHARIA DE DADOS • WORKFLOWS & RESILIÊNCIA',
      slides: [
        {
          tag: 'TESE DE NEGÓCIO & KPIS',
          headline: 'Automação Contínua e Detecção Precoce de Falhas Operacionais',
          subtext: 'Substituição de rotinas operacionais manuais por um orquestrador resiliente em n8n e Python, garantindo SLA de 99.8% e notificações em tempo real.',
          type: 'kpis',
          kpis: [
            { label: 'Tempo Poupado', value: '-18h', desc: 'Horas semanais de trabalho manual redirecionadas', colorClass: 'text-emerald-400' },
            { label: 'Detecção de Erro', value: '< 5 min', desc: 'Identificação de quebra de integração em tempo real', colorClass: 'text-sky-400' },
            { label: 'SLA de Disponibilidade', value: '99.8%', desc: 'Dados e relatórios entregues pontualmente aos tomadores', colorClass: 'text-cyan-400' },
            { label: 'Processos Automatizados', value: '100%', desc: 'Esteiras de conciliação e alertas rodando sem intervenção', colorClass: 'text-amber-400' }
          ]
        },
        {
          tag: 'RAIO-X DO PROBLEMA',
          headline: 'Reatividade a Incidentes e Degradação de Confiança Técnica',
          subtext: 'Descobrir falhas em cargas de dados através de reclamações de diretores gerava estresse e paralisações operacionais críticas.',
          type: 'pains',
          pains: [
            { icon: '🚨', title: 'Notificação Tardia de Incidentes', desc: 'APIs externas de parceiros caíam durante a madrugada e o time só descobria no meio da manhã com relatórios em branco.', impact: 'Atraso em decisões do C-Level' },
            { icon: '⚙️', title: 'Sobrecarga de Tarefas Repetitivas', desc: 'Engenheiros e analistas dedicavam manhãs inteiras executando scripts pontuais e corrigindo dados corrompidos manualmente.', impact: 'Custo de oportunidade técnico elevado' },
            { icon: '🔍', title: 'Falta de Rastreabilidade e Logs', desc: 'Inexistência de histórico centralizado de execuções, exigindo horas de depuração para encontrar o ponto exato da quebra.', impact: 'MTTR superior a 4 horas' }
          ]
        },
        {
          tag: 'ARQUITETURA & ENGENHARIA',
          headline: 'Orquestrador n8n, Validação em Python & Webhooks no Slack',
          subtext: 'Fluxos idempotentes com detecção estatística de anomalias (Z-Score) e escalonamento automático de alertas.',
          type: 'architecture',
          badges: ['n8n Orchestrator', 'Python Scripting', 'PostgreSQL', 'Slack API Webhooks', 'Z-Score Anomaly Detection', 'Docker'],
          phases: [
            { phase: 'Orquestração', title: 'Workflows em n8n', desc: 'Triggers temporais e webhook listeners orquestrando sequências de scripts com retentativas automáticas.', codeSnippet: 'n8n_flow: Trigger -> Execute -> Validate' },
            { phase: 'Algoritmo Estatístico', title: 'Detector de Anomalias', desc: 'Cálculo de desvio padrão móvel sobre volumes transacionais com alerta quando Z-Score > 2.5.', codeSnippet: 'z_score = (valor_atual - media_movel) / desvio' },
            { phase: 'Notificação Ativa', title: 'Slack Interactive Payload', desc: 'Envio de card formatado no canal de engenharia com métricas, contexto do erro e link de resolução.', codeSnippet: 'postSlackAlert(channel="#data-ops", payload)' }
          ]
        },
        {
          tag: 'IMPACTO & RECOMENDAÇÕES',
          headline: 'Retorno sobre Investimento Consolidado & Próximos Passos',
          subtext: 'Segurança operacional garantida e liberação de tempo técnico para projetos analíticos de alto valor.',
          type: 'roadmap',
          roadmap: [
            { horizon: '30 DIAS', timing: 'Curto Prazo', action: 'Calibração de Z-Score Sazonal', detail: 'Ajuste fino do detector de anomalias considerando feriados nacionais e variações sazonais de pico.', expectedRoi: 'Zero falsos positivos em finais de semana', borderClass: 'border-emerald-500', textClass: 'text-emerald-400' },
            { horizon: '90 DIAS', timing: 'Médio Prazo', action: 'Dead Letter Queue (DLQ)', detail: 'Fila isolada para reprocessamento automático e seguro de pacotes rejeitados por instabilidade de rede.', expectedRoi: 'Idempotência integral em cargas assíncronas', borderClass: 'border-sky-500', textClass: 'text-sky-400' },
            { horizon: '180 DIAS', timing: 'Longo Prazo', action: 'Arquitetura Serverless Distribuída', detail: 'Migração dos orquestradores para cluster em Kubernetes com auto-scaling sob alta demanda de processamento.', expectedRoi: 'SLA de 99.99% para volumes massivos', borderClass: 'border-indigo-500', textClass: 'text-indigo-400' }
          ]
        }
      ]
    },

    rfm: {
      title: '01. Cockpit Analítico RFM & Prevenção de Churn em Vendas',
      category: 'CRM & MACHINE INTELLIGENCE • REVENUE OPERATIONS',
      slides: [
        {
          tag: 'TESE DE NEGÓCIO & KPIS',
          headline: 'Segmentação Científica de Clientes e Proteção de Receita',
          subtext: 'Estratificação matemática da base por Recência, Frequência e Valor Monetário, revelando clusters táticos para ativação comercial com alto ROI.',
          type: 'kpis',
          kpis: [
            { label: 'Receita Protegida', value: 'R$ 485k', desc: 'Montante em risco imediato salvo com ações direcionadas', colorClass: 'text-rose-400' },
            { label: 'Taxa de Reativação', value: '+35%', desc: 'Sucesso no resgate de clientes em risco com playbook', colorClass: 'text-emerald-400' },
            { label: 'Clusters Mapeados', value: '11', desc: 'Segmentos comportamentais acionáveis em tempo real', colorClass: 'text-sky-400' },
            { label: 'Clientes Analisados', value: '800', desc: '100% da base ativa classificada por quantis matemáticos', colorClass: 'text-cyan-400' }
          ]
        },
        {
          tag: 'RAIO-X DO PROBLEMA',
          headline: 'Abordagem Homogênea em Base Heterogênea e Evasão Silenciosa',
          subtext: 'Tratar todos os clientes de forma idêntica causava desperdício de verba de marketing e negligência com contas altamente lucrativas.',
          type: 'pains',
          pains: [
            { icon: '💸', title: 'Desconto Inadequado para Campeões', desc: 'Envio de cupons promocionais agressivos para clientes fiéis que comprariam sem necessidade de incentivo de preço.', impact: 'Erosão de margem bruta' },
            { icon: '🚪', title: 'Evasão Silenciosa de Contas VIP', desc: 'Compradores frequentes paravam de comprar gradualmente sem que nenhum alerta fosse emitido para o time de contas.', impact: '24.8% da receita em risco' },
            { icon: '🎯', title: 'Falta de Priorização Comercial', desc: 'Vendedores contatavam clientes aleatoriamente ou focavam em contas frias sem propensão de retorno financeiro.', impact: 'Produtividade de vendas diluída' }
          ]
        },
        {
          tag: 'ARQUITETURA & ENGENHARIA',
          headline: 'Modelagem RFM por Quantis, Streamlit & Visualização 3D',
          subtext: 'Algoritmo em Python calculando escores relativos de 1 a 5, cruzamento matricial e interface visual interativa para times de negócio.',
          type: 'architecture',
          badges: ['Python 3.11', 'Streamlit Web UI', 'Plotly 3D Scatter', 'Pandas qcut Quantiles', 'CRM Playbooks', 'RFM Scoring'],
          phases: [
            { phase: 'Cálculo de Métricas', title: 'Recência, Frequência & Valor', desc: 'Extração da data da última compra, contagem de pedidos e somatório do ticket por cliente.', codeSnippet: 'rfm = df.groupby("id").agg({"data":"max", ...})' },
            { phase: 'Quantização Estatística', title: 'Quintis Relativos (pd.qcut)', desc: 'Divisão balanceada em notas de 1 a 5 eliminando distorções de outliers e caudas longas.', codeSnippet: 'pd.qcut(rfm["recencia"], q=5, labels=[5,4,3,2,1])' },
            { phase: 'Classificação em Clusters', title: 'Mapeamento Heurístico', desc: 'Segmentação em 11 personas (Campeões, Leais, Em Risco, Hibernando) com playbooks dedicados.', codeSnippet: 'assign_cluster(score_r, score_f, score_m)' }
          ]
        },
        {
          tag: 'IMPACTO & RECOMENDAÇÕES',
          headline: 'Retorno sobre Investimento Consolidado & Próximos Passos',
          subtext: 'Geração imediata de caixa e estruturação de inteligência preditiva para maximização do valor de vida do cliente.',
          type: 'roadmap',
          roadmap: [
            { horizon: '30 DIAS', timing: 'Curto Prazo', action: 'Régua de CRM Automatizada', detail: 'Integração via Webhook para disparo automático de playbook de resgate quando o score de Recência cair abaixo de 3.', expectedRoi: 'Reativação de 35% dos clientes em risco', borderClass: 'border-emerald-500', textClass: 'text-emerald-400' },
            { horizon: '90 DIAS', timing: 'Médio Prazo', action: 'Modelo de Propensão (LightGBM)', detail: 'Algoritmo preditivo estimando a probabilidade de recompra nos próximos 30 dias com base no histórico.', expectedRoi: 'Precisão comercial de 88%', borderClass: 'border-sky-500', textClass: 'text-sky-400' },
            { horizon: '180 DIAS', timing: 'Longo Prazo', action: 'Motor de Next Best Action (NBA)', detail: 'Recomendação personalizada de produtos e precificação dinâmica para o cluster Campeões e Leais.', expectedRoi: 'Expansão de 20% no ticket médio', borderClass: 'border-indigo-500', textClass: 'text-indigo-400' }
          ]
        }
      ]
    }
  };

  let currentDeckKey = 'logistica';
  let currentSlideIndex = 0;
  let isDeckOpen = false;

  function renderSlide(deckKey, slideIdx) {
    const titleEl = document.getElementById('deckCaseTitle');
    const progressEl = document.getElementById('deckProgress');
    const contentEl = document.getElementById('deckSlideContent');
    const dotsContainer = document.getElementById('deckDots');
    const prevBtn = document.getElementById('prevSlideBtn');
    const nextBtn = document.getElementById('nextSlideBtn');

    if (!contentEl) return;

    const deck = DECKS_DATA[deckKey] || DECKS_DATA.logistica;
    const slides = deck.slides;
    const slide = slides[slideIdx];

    if (titleEl) titleEl.textContent = deck.title.toUpperCase();
    if (progressEl) progressEl.textContent = `Slide ${slideIdx + 1} de ${slides.length}`;

    // Render Dots
    if (dotsContainer) {
      dotsContainer.innerHTML = slides.map((_, i) => `
        <div class="deck-dot ${i === slideIdx ? 'active' : ''}" data-index="${i}" title="Ir para slide ${i + 1}"></div>
      `).join('');

      dotsContainer.querySelectorAll('.deck-dot').forEach(d => {
        d.addEventListener('click', (e) => {
          const idx = parseInt(e.currentTarget.getAttribute('data-index'), 10);
          goToSlide(idx);
        });
      });
    }

    // Update prev/next button state
    if (prevBtn) {
      prevBtn.disabled = slideIdx === 0;
      prevBtn.style.opacity = slideIdx === 0 ? '0.4' : '1';
      prevBtn.style.cursor = slideIdx === 0 ? 'not-allowed' : 'pointer';
    }

    if (nextBtn) {
      nextBtn.innerHTML = slideIdx === slides.length - 1 
        ? '<span>Concluir ✕</span>' 
        : '<span>Próximo →</span>';
    }

    // Render Slide Content based on type
    let bodyHtml = '';

    if (slide.type === 'kpis') {
      bodyHtml = `
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 my-auto">
          ${slide.kpis.map(k => `
            <div class="p-4 sm:p-5 rounded-2xl bg-neutral-900/90 border border-neutral-800/90 flex flex-col justify-between shadow-lg hover:border-neutral-700 transition-colors">
              <span class="text-[10px] sm:text-[11px] font-mono uppercase tracking-wider text-neutral-400 font-medium">${k.label}</span>
              <span class="text-2xl sm:text-3xl lg:text-4xl font-extrabold font-mono ${k.colorClass} my-2 tracking-tight">${k.value}</span>
              <span class="text-[11px] text-neutral-300 leading-snug">${k.desc}</span>
            </div>
          `).join('')}
        </div>
      `;
    } else if (slide.type === 'pains') {
      bodyHtml = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-auto">
          ${slide.pains.map(p => `
            <div class="p-5 rounded-2xl bg-neutral-900/90 border border-neutral-800/90 flex flex-col justify-between space-y-3 shadow-lg hover:border-neutral-700 transition-colors">
              <div class="flex items-center gap-2.5">
                <div class="w-8 h-8 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 text-sm font-bold flex-shrink-0">
                  ${p.icon}
                </div>
                <h4 class="text-sm font-bold text-white leading-tight">${p.title}</h4>
              </div>
              <p class="text-xs text-neutral-300 leading-relaxed flex-1">${p.desc}</p>
              <div class="pt-2 border-t border-neutral-800/80 flex items-center justify-between text-[11px] font-mono text-rose-400">
                <span>Vazamento Operacional:</span>
                <strong class="font-bold">${p.impact}</strong>
              </div>
            </div>
          `).join('')}
        </div>
      `;
    } else if (slide.type === 'architecture') {
      bodyHtml = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-auto">
          ${slide.phases.map((a, idx) => `
            <div class="p-5 rounded-2xl bg-neutral-900/90 border border-neutral-800/90 flex flex-col justify-between space-y-3 shadow-lg hover:border-neutral-700 transition-colors">
              <div class="flex items-center justify-between">
                <span class="w-6 h-6 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 font-mono text-xs font-bold flex items-center justify-center">${idx + 1}</span>
                <span class="text-[10px] font-mono text-neutral-500 uppercase tracking-wider">${a.phase}</span>
              </div>
              <div>
                <h4 class="text-sm font-bold text-white mb-1.5">${a.title}</h4>
                <p class="text-xs text-neutral-300 leading-relaxed">${a.desc}</p>
              </div>
              <div class="p-2.5 rounded-lg bg-black/50 border border-neutral-800 text-[10px] font-mono text-indigo-300 truncate">
                ${a.codeSnippet}
              </div>
            </div>
          `).join('')}
        </div>
      `;
    } else if (slide.type === 'roadmap') {
      bodyHtml = `
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-auto">
          ${slide.roadmap.map(r => `
            <div class="p-5 rounded-2xl bg-neutral-900/90 border border-neutral-800/90 flex flex-col justify-between space-y-2.5 shadow-lg border-t-2 ${r.borderClass}">
              <div class="flex items-center justify-between">
                <span class="text-[10px] font-mono uppercase font-bold tracking-wider ${r.textClass}">${r.horizon}</span>
                <span class="text-[10px] font-mono text-neutral-500">${r.timing}</span>
              </div>
              <h4 class="text-sm font-bold text-white">${r.action}</h4>
              <p class="text-xs text-neutral-300 leading-relaxed flex-1">${r.detail}</p>
              <div class="pt-2 border-t border-neutral-800/80 text-[11px] font-mono font-semibold ${r.textClass}">
                Resultado: ${r.expectedRoi}
              </div>
            </div>
          `).join('')}
        </div>
      `;
    }

    contentEl.innerHTML = `
      <div class="deck-slide-animated h-full flex flex-col justify-between">
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="px-2.5 py-0.5 rounded-full text-[10px] font-mono tracking-wider uppercase bg-sky-500/10 text-sky-400 border border-sky-500/20 font-bold">ETAPA ${slideIdx + 1} DE 4 • ${slide.tag}</span>
            <span class="text-[11px] text-neutral-500 font-mono hidden sm:inline">•</span>
            <span class="text-[11px] text-neutral-400 font-mono hidden sm:inline">${deck.category}</span>
          </div>
          <h2 class="text-xl sm:text-2xl lg:text-3xl font-extrabold text-white tracking-tight leading-tight mb-2">${slide.headline}</h2>
          <p class="text-xs sm:text-sm text-neutral-400 max-w-3xl leading-relaxed">${slide.subtext}</p>
          ${slide.badges ? `
            <div class="flex flex-wrap gap-1.5 pt-2">
              ${slide.badges.map(b => `<span class="tech-badge text-[11px] !py-0.5 !px-2.5">${b}</span>`).join('')}
            </div>
          ` : ''}
        </div>

        ${bodyHtml}

        <div class="flex items-center justify-between text-[11px] text-neutral-500 font-mono pt-3 border-t border-neutral-800/60">
          <span class="truncate">Fernando Cavalcante • Analista de Dados &amp; Especialista em BI</span>
          <span class="hidden sm:inline">Navegue com Setas [← / →] ou Espaço • [ESC] para fechar</span>
        </div>
      </div>
    `;
  }

  function openDeck(deckKey) {
    ensureDeckStyles();
    const modal = ensureDeckModal();
    currentDeckKey = deckKey || 'logistica';
    currentSlideIndex = 0;
    isDeckOpen = true;
    renderSlide(currentDeckKey, currentSlideIndex);
    modal.classList.remove('hidden');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeDeck() {
    const modal = document.getElementById('deckViewerModal');
    if (!modal) return;
    modal.classList.add('hidden');
    modal.classList.remove('active');
    document.body.style.overflow = '';
    isDeckOpen = false;
  }

  function goToSlide(idx) {
    const deck = DECKS_DATA[currentDeckKey] || DECKS_DATA.logistica;
    if (idx < 0) return;
    if (idx >= deck.slides.length) {
      closeDeck();
      return;
    }
    currentSlideIndex = idx;
    renderSlide(currentDeckKey, currentSlideIndex);
  }

  function initDeckViewer() {
    ensureDeckStyles();
    const modal = ensureDeckModal();
    const closeBtn = document.getElementById('closeDeckBtn');
    const prevBtn = document.getElementById('prevSlideBtn');
    const nextBtn = document.getElementById('nextSlideBtn');

    // Delegate click on open-deck-btn anywhere on document
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('.open-deck-btn');
      if (btn) {
        e.preventDefault();
        const deckKey = btn.getAttribute('data-deck') || 'logistica';
        openDeck(deckKey);
      }
    });

    if (closeBtn) closeBtn.addEventListener('click', closeDeck);

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        goToSlide(currentSlideIndex - 1);
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        goToSlide(currentSlideIndex + 1);
      });
    }

    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeDeck();
    });

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {
      if (!isDeckOpen) return;

      if (e.key === 'ArrowRight' || e.code === 'Space') {
        e.preventDefault();
        goToSlide(currentSlideIndex + 1);
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        goToSlide(currentSlideIndex - 1);
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeDeck();
      }
    });
  }

  // Expor globalmente
  window.openExecutiveDeck = openDeck;
  window.initExecutiveDeckViewer = initDeckViewer;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDeckViewer);
  } else {
    initDeckViewer();
  }
})();
