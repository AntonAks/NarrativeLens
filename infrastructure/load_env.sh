#!/bin/bash
# load_env.sh - Script to load environment variables from .env file

# Check if .env file exists
if [ -f ../.env ]; then
  export $(grep -v '^#' ../.env | xargs)
  echo "Environment variables loaded from .env file"
else
  echo "Warning: .env file not found"
fi

# Export variables for Terraform

export TF_VAR_aws_region=${AWS_REGION}
export TF_VAR_news_data_bucket_name=${S3_PREFIX}-${NEWS_DATA_BUCKET_NAME}-${ENVIRONMENT}
export TF_VAR_headlines_data_bucket_name=${S3_PREFIX}-${HEADLINES_DATA_BUCKET_NAME}-${ENVIRONMENT}
export TF_VAR_lambda_code_bucket_name=${S3_PREFIX}-${LAMBDA_CODE_BUCKET_NAME}-${ENVIRONMENT}
export TF_VAR_lambda_packages_dir=${LAMBDA_PACKAGES_DIR}


# Run terraform with all arguments passed to this script
terraform $@