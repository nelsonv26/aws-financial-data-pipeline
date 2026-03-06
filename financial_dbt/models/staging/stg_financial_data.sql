SELECT *
FROM {{ source('financial_raw','processed_finance_parquet') }}