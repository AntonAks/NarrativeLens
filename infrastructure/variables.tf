# variables.tf - Variables for the News Analyzer infrastructure

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-central-1"
}

variable "news_data_bucket_name" {
  description = "Name of the S3 bucket to store news data"
  type        = string
  default     = "news-analyzer-data-bucket"
}

variable "lambda_code_bucket_name" {
  description = "Name of the S3 bucket to store Lambda code and layers"
  type        = string
  default     = "news-analyzer-lambda-code"
}

variable "lambda_packages_dir" {
  description = "Directory containing Lambda packages"
  type        = string
  default     = "../lambda_packages"
}