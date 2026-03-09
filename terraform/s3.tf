resource "aws_s3_bucket" "data_lake" {
  bucket = "nelson-aws-financial-data-lake"

  tags = {
    Name = "Financial Data Lake"
  }
}