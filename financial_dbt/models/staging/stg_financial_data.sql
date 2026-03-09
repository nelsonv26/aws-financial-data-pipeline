SELECT
    stock_index,
    CAST(date AS DATE) as date,
    open_price,
    high_price,
    low_price,
    close_price,
    trading_volume
FROM {{ source('financial_data_lake', 'processed_finance_parquet') }}