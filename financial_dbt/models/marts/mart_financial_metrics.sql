SELECT
    stock_index,
    year(date) as year,
    avg(close_price) as avg_close_price,
    sum(trading_volume) as total_volume
FROM {{ ref('stg_financial_data') }}
GROUP BY 1,2