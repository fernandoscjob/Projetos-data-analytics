-- =============================================================================
-- PROJETO: AUDITORIA CONTRATUAL DE FRETES & RECUPERAÇÃO DE GLOSAS
-- MOTOR: Google BigQuery / PostgreSQL
-- OBJETIVO: Recalcular o peso cubado, aplicar tabelas tarifárias vigentes
--           e apontar divergências financeiras acima da tolerância contratual.
-- =============================================================================

WITH CteNormalizados AS (
    SELECT 
        cte.numero_cte,
        cte.chave_acesso,
        cte.transportadora_id,
        cte.data_emissao,
        cte.uf_origem,
        cte.uf_destino,
        cte.peso_bruto_declarado_kg,
        cte.volume_m3,
        cte.valor_mercadoria,
        cte.valor_faturado_transportadora,
        -- Extração do ano/mês para partição analítica
        DATE_TRUNC(cte.data_emissao, MONTH) AS mes_emissao
    FROM `projeto_dados.bronze_logistica.conhecimentos_transporte` cte
    WHERE cte.status_cte = 'AUTORIZADO'
),

TabelaContratualVigente AS (
    SELECT 
        tab.transportadora_id,
        tab.uf_destino,
        tab.tarifa_base_fixa,
        tab.preco_excedente_kg,
        tab.fator_cubagem_m3,          -- Geralmente 300 kg/m³ para rodoviário fracionado
        tab.aliquota_gris_seguro,       -- Ex: 0.003 (0.3% sobre valor da NF)
        tab.tarifa_pedagio_fracao_100kg,
        tab.vigencia_inicio,
        tab.vigencia_fim
    FROM `projeto_dados.silver_contratos.tabelas_tarifarias` tab
    WHERE tab.ativo = TRUE
),

CalculoAuditado AS (
    SELECT 
        c.numero_cte,
        c.transportadora_id,
        c.data_emissao,
        c.valor_faturado_transportadora,
        c.peso_bruto_declarado_kg,
        c.volume_m3,
        
        -- 1. Cálculo da Cubagem Contratada
        (c.volume_m3 * t.fator_cubagem_m3) AS peso_cubado_kg,
        
        -- 2. Peso Tarifado Efetivo (Maior entre real e cubado)
        GREATEST(c.peso_bruto_declarado_kg, (c.volume_m3 * t.fator_cubagem_m3)) AS peso_tarifado_esperado_kg,
        
        -- 3. Componentes da Tarifa Contratual
        t.tarifa_base_fixa,
        (GREATEST(c.peso_bruto_declarado_kg, (c.volume_m3 * t.fator_cubagem_m3)) * t.preco_excedente_kg) AS valor_peso_excedente,
        (c.valor_mercadoria * t.aliquota_gris_seguro) AS valor_gris_esperado,
        (CEIL(GREATEST(c.peso_bruto_declarado_kg, (c.volume_m3 * t.fator_cubagem_m3)) / 100.0) * t.tarifa_pedagio_fracao_100kg) AS valor_pedagio_esperado,
        
        -- 4. Valor Total Devido
        (
            t.tarifa_base_fixa + 
            (GREATEST(c.peso_bruto_declarado_kg, (c.volume_m3 * t.fator_cubagem_m3)) * t.preco_excedente_kg) +
            (c.valor_mercadoria * t.aliquota_gris_seguro) +
            (CEIL(GREATEST(c.peso_bruto_declarado_kg, (c.volume_m3 * t.fator_cubagem_m3)) / 100.0) * t.tarifa_pedagio_fracao_100kg)
        ) AS valor_devido_contratual

    FROM CteNormalizados c
    INNER JOIN TabelaContratualVigente t
        ON c.transportadora_id = t.transportadora_id
        AND c.uf_destino = t.uf_destino
        AND c.data_emissao BETWEEN t.vigencia_inicio AND t.vigencia_fim
)

-- Visão Final de Divergências e Contestação de Glosas
SELECT 
    ca.numero_cte,
    ca.transportadora_id,
    ca.data_emissao,
    ROUND(ca.valor_faturado_transportadora, 2) AS valor_faturado,
    ROUND(ca.valor_devido_contratual, 2) AS valor_devido,
    ROUND(ca.valor_faturado_transportadora - ca.valor_devido_contratual, 2) AS divergencia_glosa,
    ROUND(((ca.valor_faturado_transportadora - ca.valor_devido_contratual) / ca.valor_devido_contratual) * 100.0, 1) AS percentual_sobretaxa,
    CASE 
        WHEN (ca.valor_faturado_transportadora - ca.valor_devido_contratual) > 10.00 THEN 'GLOSA - CONTESTAR FATURA'
        WHEN (ca.valor_faturado_transportadora - ca.valor_devido_contratual) BETWEEN -5.00 AND 10.00 THEN 'APROVADO - DENTRO DA TOLERANCIA'
        ELSE 'REVISAO MANUAL'
    END AS status_auditoria
FROM CalculoAuditado ca
ORDER BY divergencia_glosa DESC;
