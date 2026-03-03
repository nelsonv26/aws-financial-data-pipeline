# aws-financial-data-pipeline
## Architecture Implemented

- S3 Data Lake (raw / processed / processed_partitioned)
- Data cleaning and normalization in Python
- Hive-style partitioning by year
- Athena external table
- Athena partitioned table with MSCK REPAIR
- Query performance optimization via partition pruning