resource "aws_s3_bucket" "data_lake" {
  bucket = "nelson-financial-data-lake-001"

  tags = {
    Name = "Financial Data Lake"
  }
}