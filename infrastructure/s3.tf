# S3 bucket for storing news data
resource "aws_s3_bucket" "news_data_bucket" {
  bucket = var.news_data_bucket_name
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_s3_bucket_ownership_controls" "news_data_bucket_ownership" {
  bucket = aws_s3_bucket.news_data_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "news_data_bucket_public_access" {
  bucket                  = aws_s3_bucket.news_data_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# S3 bucket for Lambda code and layers
resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket = var.lambda_code_bucket_name
}

resource "aws_s3_bucket_ownership_controls" "lambda_code_bucket_ownership" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "lambda_code_bucket_public_access" {
  bucket                  = aws_s3_bucket.lambda_code_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}