{{ config(
    materialized = "table",
    schema = "gold_analytics",
    tags = ["dimensao", "clientes", "ssot"]
) }}

WITH StagingClientes AS (
    SELECT 
        cliente_id,
        TRIM(UPPER(nome_razao_social)) AS nome_cliente,
        email_corporativo,
        segmento_mercado,
        cidade,
        uf,
        regiao,
        data_cadastro,
        data_primeira_compra,
        ativo AS is_ativo
    FROM {{ ref("stg_crm_clientes") }}
)

SELECT 
    -- Surrogate Key (Chave Substituta Inteira)
    FARM_FINGERPRINT(cliente_id) AS sk_cliente,
    cliente_id AS bk_cliente,
    nome_cliente,
    email_corporativo,
    COALESCE(segmento_mercado, 'NAO_INFORMADO') AS segmento_mercado,
    cidade,
    uf,
    regiao,
    data_cadastro,
    data_primeira_compra,
    is_ativo,
    CURRENT_TIMESTAMP() AS dbt_updated_at
FROM StagingClientes;
