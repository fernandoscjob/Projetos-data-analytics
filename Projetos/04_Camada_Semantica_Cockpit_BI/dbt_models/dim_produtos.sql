{{ config(
    materialized = "table",
    schema = "gold_analytics",
    tags = ["dimensao", "produtos"]
) }}

SELECT 
    FARM_FINGERPRINT(sku) AS sk_produto,
    sku AS bk_sku,
    nome_produto,
    categoria,
    subcategoria,
    unidade_medida,
    preco_custo_padrao,
    preco_tabela_sugerido,
    is_ativo,
    CURRENT_TIMESTAMP() AS dbt_updated_at
FROM {{ ref("stg_erp_produtos") }};
