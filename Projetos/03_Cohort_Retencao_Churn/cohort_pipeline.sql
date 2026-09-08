-- =============================================================================
-- PROJETO: MODELAGEM DE COHORT, RETENÇÃO LONGITUDINAL & CHURN
-- MOTOR: dbt / Google BigQuery / PostgreSQL
-- OBJETIVO: Criar a matriz dimensional de safras com First-Touch Attribution,
--           calculando a retenção mensal relativa (M0 a M12+) e taxas de evasão.
-- =============================================================================

WITH ClientesSafra AS (
    -- 1. Identifica a data e o mês da 1ª compra/assinatura de cada cliente
    SELECT 
        cliente_id,
        DATE_TRUNC(MIN(data_compra), MONTH) AS safra_mes
    FROM `projeto_dados.gold_vendas.fct_transacoes`
    WHERE status_pagamento = 'CONCLUIDO'
    GROUP BY cliente_id
),

AtividadeMensal AS (
    -- 2. Mapeia todos os meses em que o cliente realizou compras ativas
    SELECT DISTINCT
        t.cliente_id,
        s.safra_mes,
        DATE_TRUNC(t.data_compra, MONTH) AS mes_atividade,
        -- Diferença em meses entre o mês da atividade e o mês de entrada
        DATE_DIFF(DATE_TRUNC(t.data_compra, MONTH), s.safra_mes, MONTH) AS periodo_m
    FROM `projeto_dados.gold_vendas.fct_transacoes` t
    INNER JOIN ClientesSafra s 
        ON t.cliente_id = s.cliente_id
    WHERE t.status_pagamento = 'CONCLUIDO'
),

TamanhoSafras AS (
    -- 3. Contagem do volume inicial de clientes de cada safra (M0)
    SELECT 
        safra_mes, 
        COUNT(DISTINCT cliente_id) AS total_clientes_m0
    FROM ClientesSafra
    GROUP BY safra_mes
)

-- 4. Matriz Final de Retenção & Churn Longitudinal
SELECT 
    a.safra_mes,
    s.total_clientes_m0,
    a.periodo_m,
    COUNT(DISTINCT a.cliente_id) AS clientes_ativos,
    -- Taxa de Retenção %
    ROUND(COUNT(DISTINCT a.cliente_id) * 100.0 / s.total_clientes_m0, 1) AS taxa_retencao_pct,
    -- Taxa de Churn Acumulada %
    ROUND(100.0 - (COUNT(DISTINCT a.cliente_id) * 100.0 / s.total_clientes_m0), 1) AS taxa_churn_acumulado_pct
FROM AtividadeMensal a
INNER JOIN TamanhoSafras s 
    ON a.safra_mes = s.safra_mes
GROUP BY a.safra_mes, s.total_clientes_m0, a.periodo_m
ORDER BY a.safra_mes ASC, a.periodo_m ASC;
