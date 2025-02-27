# main.tf - AWS Lambda Infrastructure for News Analyzer
provider "aws" {
  region = var.aws_region
}

# Upload Lambda layer to S3
resource "aws_s3_object" "lambda_layer_upload" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  key    = "layers/news_parser_layer.zip"
  source = "${var.lambda_packages_dir}/layer.zip"
  etag   = filemd5("${var.lambda_packages_dir}/layer.zip")
}

# Lambda Layer containing shared dependencies (from S3)
resource "aws_lambda_layer_version" "news_parser_layer" {
  layer_name          = "news_parser_layer"
  description         = "Common dependencies for news parser lambdas"
  s3_bucket           = aws_s3_bucket.lambda_code_bucket.id
  s3_key              = aws_s3_object.lambda_layer_upload.key
  compatible_runtimes = ["python3.12"]
}

# Upload Lambda function zips to S3
resource "aws_s3_object" "cnn_lambda_upload" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  key    = "functions/cnn.zip"
  source = "${var.lambda_packages_dir}/cnn.zip"
  etag   = filemd5("${var.lambda_packages_dir}/cnn.zip")
}

resource "aws_s3_object" "liga_lambda_upload" {
  bucket = aws_s3_bucket.lambda_code_bucket.id
  key    = "functions/liga.zip"
  source = "${var.lambda_packages_dir}/liga.zip"
  etag   = filemd5("${var.lambda_packages_dir}/liga.zip")
}

# IAM role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "news_parser_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

# IAM policy attachment for Lambda execution
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom IAM policy for S3 access
resource "aws_iam_policy" "lambda_s3_policy" {
  name        = "news_parser_s3_access"
  description = "Allow Lambda functions to access S3 buckets"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.news_data_bucket.arn,
          "${aws_s3_bucket.news_data_bucket.arn}/*",
          aws_s3_bucket.lambda_code_bucket.arn,
          "${aws_s3_bucket.lambda_code_bucket.arn}/*"
        ]
      }
    ]
  })
}

# Attach S3 policy to Lambda role
resource "aws_iam_role_policy_attachment" "lambda_s3_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3_policy.arn
}

# CNN Parser Lambda function
resource "aws_lambda_function" "cnn_parser" {
  function_name = "cnn_news_parser"
  description   = "Lambda function for parsing CNN news"
  s3_bucket     = aws_s3_bucket.lambda_code_bucket.id
  s3_key        = aws_s3_object.cnn_lambda_upload.key
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30
  memory_size   = 256
  role = aws_iam_role.lambda_role.arn
  layers = [aws_lambda_layer_version.news_parser_layer.arn]
  environment {
    variables = {
      NEWS_DATA_BUCKET = aws_s3_bucket.news_data_bucket.bucket
    }
  }
}

# Liga Parser Lambda function
resource "aws_lambda_function" "liga_parser" {
  function_name = "liga_news_parser"
  description   = "Lambda function for parsing Liga news"
  s3_bucket     = aws_s3_bucket.lambda_code_bucket.id
  s3_key        = aws_s3_object.liga_lambda_upload.key
  handler       = "handler.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30
  memory_size   = 256
  role = aws_iam_role.lambda_role.arn
  layers = [aws_lambda_layer_version.news_parser_layer.arn]
  environment {
    variables = {
      NEWS_DATA_BUCKET = aws_s3_bucket.news_data_bucket.bucket
    }
  }
}

# CloudWatch Log Groups for Lambda functions
resource "aws_cloudwatch_log_group" "cnn_parser_logs" {
  name              = "/aws/lambda/${aws_lambda_function.cnn_parser.function_name}"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "liga_parser_logs" {
  name              = "/aws/lambda/${aws_lambda_function.liga_parser.function_name}"
  retention_in_days = 7
}


# Create a CloudWatch Event Rule to trigger the Lambda every 5 minutes
resource "aws_cloudwatch_event_rule" "every_five_minutes" {
  name                = "every-six-hours"
  schedule_expression = "rate(120 minutes)"
}
