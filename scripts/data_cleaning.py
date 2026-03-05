import pandas as pd
import os


def clean_data(input_path: str, output_path: str) -> None:
    """
    Cleans the raw finance dataset and saves a processed version.

    Args:
        input_path (str): Path to raw CSV file.
        output_path (str): Path to save cleaned CSV file.
    """

    # Load dataset
    df = pd.read_csv(input_path)

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Clean column names
    df.columns = (
        df.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("%", "percent", regex=False)
        .str.replace("/", "_", regex=False)
    )

    # Create year column for partitioning
    df["year"] = df["date"].dt.year

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save cleaned dataset
    df.to_csv(output_path, index=False)

    print(f"Cleaned dataset saved at {output_path}")


if __name__ == "__main__":
    clean_data(
        input_path="data/raw/finance_economics_dataset.csv",
        output_path="data/processed/processed_finance_dataset.csv"
    )