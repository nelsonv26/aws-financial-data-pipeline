import pandas as pd
import os


def convert_to_parquet(input_path: str, output_dir: str) -> None:
    """
    Converts processed CSV dataset into partitioned Parquet format by year.

    Args:
        input_path (str): Path to processed CSV file.
        output_dir (str): Directory where parquet partitions will be stored.
    """

    # Load processed CSV
    df = pd.read_csv(input_path)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Partition and save as Parquet
    for year, group in df.groupby("year"):
        year_path = os.path.join(output_dir, f"year={year}")
        os.makedirs(year_path, exist_ok=True)

        group.to_parquet(
            os.path.join(year_path, f"finance_{year}.parquet"),
            index=False,
            engine="pyarrow"
        )

    print(f"Parquet dataset created successfully at {output_dir}")


if __name__ == "__main__":
    convert_to_parquet(
        input_path="data/processed/processed_finance_dataset.csv",
        output_dir="data/parquet"
    )