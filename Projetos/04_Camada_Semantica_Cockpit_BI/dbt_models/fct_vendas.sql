{{ config(
    materialized = "incremental",
    unique_key = "sk_venda_item",
    schema = "gold_analytics",
    partition_by = {
      "field": "data_emissao",
      "data_type": "date",
      "granularity": "month"
    },
    cluster_by = ["sk_cliente", "sk_produto"],
    tags = ["fato", "vendas"]
) }}

WITH VendasItem AS (
    SELECT 
        v.numero_pedido,
        v.numero_item,
        v.cliente_id,
        v.sku,
        v.vendedor_id,
        DATE(v.data_emissao) AS data_emissao,
        v.quantidade,
        v.preco_unitario_bruto,
        v.valor_desconto,
        v.valor_impostos,
        v.custo_mercadoria_vendida,
        v.valor_frete_rateado,
        v.status_pedido
    FROM {{ ref("stg_erp_vendas_itens") }} v
    {% if is_incremental() %}
        WHERE DATE(v.data_emissao) >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY)
    {% endif %}
)

SELECT 
    -- Chave Primária Substituta
    FARM_FINGERPRINT(CONCAT(numero_pedido, '-', CAST(numero_item AS STRING))) AS sk_venda_item,
    
    -- Chaves Estrangeiras Dimensionais
    CAST(FORMAT_DATE('%Y%m%d', data_emissao) AS INT64) AS sk_data,
    FARM_FINGERPRINT(cliente_id) AS sk_cliente,
    FARM_FINGERPRINT(sku) AS sk_produto,
    vendedor_id AS sk_vendedor,
    
    -- Atributos Degenerados
    numero_pedido,
    numero_item,
    data_emissao,
    status_pedido,
    
    -- Métricas e Fatos Aditivos
    quantidade,
    (quantidade * preco_unitario_bruto) AS valor_bruto,
    valor_desconto,
    ((quantidade * preco_unitario_bruto) - valor_desconto) AS valor_liquido_faturado,
    valor_impostos,
    custo_mercadoria_vendida AS cmv,
    valor_frete_rateado,
    
    -- Margem de Contribuição Atômica
    (
        ((quantidade * preco_unitario_bruto) - valor_desconto)
        - valor_impostos
        - custo_mercadoria_vendida
        - valor_frete_rateado
    ) AS margem_contribuicao_valor

FROM VendasItem;
