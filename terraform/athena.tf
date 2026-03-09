resource "aws_athena_database" "finance_db" {
  name   = "financial_data_lake"
  bucket = aws_s3_bucket.data_lake.bucket
}