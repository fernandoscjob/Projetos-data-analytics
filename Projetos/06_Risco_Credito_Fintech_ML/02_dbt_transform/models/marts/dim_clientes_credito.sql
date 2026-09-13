WITH historico_agregado AS (
    SELECT 
        SK_ID_CURR,
        COUNT(*) AS qtd_emprestimos_anteriores,
        AVG(AMT_CREDIT) AS media_credito_anterior,
        MAX(AMT_CREDIT) AS max_credito_anterior
    FROM {{ ref('stg_previous_applications') }}
    GROUP BY SK_ID_CURR
)

SELECT 
    a.*,
    COALESCE(h.qtd_emprestimos_anteriores, 0) AS qtd_emprestimos_anteriores,
    COALESCE(h.media_credito_anterior, 0.0) AS media_credito_anterior,
    COALESCE(h.max_credito_anterior, 0.0) AS max_credito_anterior
FROM {{ ref('stg_applications') }} a
LEFT JOIN historico_agregado h
  ON a.SK_ID_CURR = h.SK_ID_CURR
