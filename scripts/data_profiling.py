import pandas as pd

# Cargar dataset
df = pd.read_csv("finance_economics_dataset.csv")

print("\n--- INFO ---")
print(df.info())

print("\n--- HEAD ---")
print(df.head())

print("\n--- DESCRIBE ---")
print(df.describe(include='all'))

print("\n--- NULOS ---")
print(df.isnull().sum())