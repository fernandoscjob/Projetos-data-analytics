{{ config(
    materialized = "table",
    schema = "gold_analytics",
    tags = ["dimensao", "calendario"]
) }}

WITH Datas AS (
    SELECT 
        dia AS data_completa
    FROM UNNEST(GENERATE_DATE_ARRAY('2023-01-01', '2028-12-31', INTERVAL 1 DAY)) AS dia
)

SELECT 
    CAST(FORMAT_DATE('%Y%m%d', data_completa) AS INT64) AS sk_data,
    data_completa,
    EXTRACT(YEAR FROM data_completa) AS ano,
    EXTRACT(QUARTER FROM data_completa) AS trimestre,
    EXTRACT(MONTH FROM data_completa) AS mes,
    FORMAT_DATE('%B', data_completa) AS nome_mes,
    FORMAT_DATE('%Y-%m', data_completa) AS ano_mes,
    EXTRACT(DAY FROM data_completa) AS dia_do_mes,
    EXTRACT(DAYOFWEEK FROM data_completa) AS dia_da_semana,
    FORMAT_DATE('%A', data_completa) AS nome_dia_semana,
    CASE WHEN EXTRACT(DAYOFWEEK FROM data_completa) IN (1, 7) THEN FALSE ELSE TRUE END AS is_dia_util
FROM Datas;
