import pandas as pd
import os


def partition_data(input_path: str, output_dir: str) -> None:
    """
    Partitions processed dataset by year using Hive-style folder structure.

    Args:
        input_path (str): Path to processed CSV file.
        output_dir (str): Directory where partitioned data will be stored.
    """

    # Load processed dataset
    df = pd.read_csv(input_path)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Partition by year
    for year in df["year"].unique():
        year_path = os.path.join(output_dir, f"year={year}")
        os.makedirs(year_path, exist_ok=True)

        df[df["year"] == year].to_csv(
            os.path.join(year_path, "data.csv"),
            index=False
        )

    print(f"Dataset partitioned successfully at {output_dir}")


if __name__ == "__main__":
    partition_data(
        input_path="data/processed/processed_finance_dataset.csv",
        output_dir="data/processed_partitioned"
    )