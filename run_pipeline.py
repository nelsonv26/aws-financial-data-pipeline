from scripts.data_cleaning import clean_data
from scripts.data_partitioning import partition_data
from scripts.convert_to_parquet import convert_to_parquet
from scripts.upload_to_s3 import upload_directory_to_s3


def run_pipeline():
    print("Starting pipeline...\n")

    # 1️⃣ Cleaning
    clean_data(
        input_path="data/raw/finance_economics_dataset.csv",
        output_path="data/processed/processed_finance_dataset.csv"
    )

    # 2️⃣ Partitioning CSV
    partition_data(
        input_path="data/processed/processed_finance_dataset.csv",
        output_dir="data/processed_partitioned"
    )

    # 3️⃣ Convert to Parquet
    convert_to_parquet(
        input_path="data/processed/processed_finance_dataset.csv",
        output_dir="data/processed_parquet"
    )

    # 4️⃣ Upload to S3
    upload_directory_to_s3(
        local_dir="data/processed_parquet",
        bucket_name="nelson-aws-financial-data-lake",
        s3_prefix="processed_parquet/"
    )

    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()