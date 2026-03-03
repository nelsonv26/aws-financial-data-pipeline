import pandas as pd
import os

# Load processed CSV
df = pd.read_csv("data/processed/processed_finance_dataset.csv")

# Create parquet output directory
output_path = "data/processed_parquet"
os.makedirs(output_path, exist_ok=True)

# Partition by year
for year, group in df.groupby("year"):
    year_path = os.path.join(output_path, f"year={year}")
    os.makedirs(year_path, exist_ok=True)
    group.to_parquet(
        os.path.join(year_path, f"finance_{year}.parquet"),
        index=False
    )

print("Parquet partitioned dataset created successfully.")