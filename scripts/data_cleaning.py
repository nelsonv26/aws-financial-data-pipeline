import pandas as pd

# Cargar dataset
df = pd.read_csv("finance_economics_dataset.csv")

# 1️⃣ Convertir Date a datetime
df["Date"] = pd.to_datetime(df["Date"])

# 2️⃣ Limpiar nombres de columnas
df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "", regex=False)
    .str.replace(")", "", regex=False)
    .str.replace("%", "percent", regex=False)
    .str.replace("/", "_", regex=False)
)

# 3️⃣ Crear columna year (para particionado futuro)
df["year"] = df["date"].dt.year

# 4️⃣ Guardar versión limpia
df.to_csv("processed_finance_dataset.csv", index=False)

print("Dataset cleaned and saved successfully.")