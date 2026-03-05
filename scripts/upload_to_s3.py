import os
import boto3


def upload_directory_to_s3(local_dir: str, bucket_name: str, s3_prefix: str) -> None:
    """
    Uploads a local directory recursively to an S3 bucket.

    Args:
        local_dir (str): Path to local folder.
        bucket_name (str): S3 bucket name.
        s3_prefix (str): Folder path inside bucket.
    """

    s3 = boto3.client("s3")

    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)

            # Preserve folder structure
            relative_path = os.path.relpath(local_path, local_dir)
            s3_path = os.path.join(s3_prefix, relative_path).replace("\\", "/")

            s3.upload_file(local_path, bucket_name, s3_path)

            print(f"Uploaded {local_path} to s3://{bucket_name}/{s3_path}")

    print("Upload completed successfully.")


if __name__ == "__main__":
    upload_directory_to_s3(
        local_dir="data/parquet",
        bucket_name="nelson-aws-financial-data-lake",
        s3_prefix="parquet/"
    )