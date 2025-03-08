# outputs.tf - Output values from the News Analyzer infrastructure

output "cnn_parser_lambda_arn" {
  description = "ARN of the CNN News Parser Lambda function"
  value       = aws_lambda_function.cnn_parser.arn
}

output "liga_parser_lambda_arn" {
  description = "ARN of the Liga News Parser Lambda function"
  value       = aws_lambda_function.liga_parser.arn
}

output "headline_collector_lambda_arn" {
  description = "ARN of the Liga News Parser Lambda function"
  value       = aws_lambda_function.headline_collector.arn
}

output "news_data_bucket_name" {
  description = "Name of the S3 bucket for news data"
  value       = aws_s3_bucket.news_data_bucket.bucket
}

output "headlines_data_bucket_name" {
  description = "Name of the S3 bucket for news data"
  value       = aws_s3_bucket.headlines_data_bucket.bucket
}

output "lambda_layer_arn" {
  description = "ARN of the Lambda layer containing shared dependencies"
  value       = aws_lambda_layer_version.news_parser_layer.arn
}