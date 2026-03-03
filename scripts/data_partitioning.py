import pandas as pd
import os

# Cargar dataset limpio
df = pd.read_csv("data/processed/processed_finance_dataset.csv")

# Crear carpeta base
base_path = "data/processed_partitioned"

if not os.path.exists(base_path):
    os.makedirs(base_path)

# Particionar por año
for year in df["year"].unique():
    year_path = f"{base_path}/year={year}"
    os.makedirs(year_path, exist_ok=True)

    df[df["year"] == year].to_csv(
        f"{year_path}/data.csv",
        index=False
    )

print("Dataset partitioned successfully.")