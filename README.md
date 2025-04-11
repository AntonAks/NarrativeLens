# NarrativeLens

## Overview
NarrativeLens is a serverless AWS application that processes and analyzes narratives using a combination of collectors, parsers, and analyzers implemented as AWS Lambda functions.

![Project Architecture](diagrams/Project%20diagram.drawio.png)

## Project Structure
NarrativeLens/
├── .env # Environment variables
├── .env.example # Example environment variables template
├── Makefile # Build and deployment automation
├── diagrams/ # Project architecture diagrams
│ └── Project diagram.drawio(.png)
├── infrastructure/ # Terraform IaC configurations
│ ├── main.tf # Main Terraform configuration
│ ├── s3.tf # S3 bucket configurations
│ ├── scheduler.tf # EventBridge scheduler config
│ ├── variables.tf # Terraform variables
│ ├── outputs.tf # Terraform outputs
│ └── load_env.sh # Environment loader script
├── lambda_functions/ # AWS Lambda function code
│ ├── analyzers/ # Text analysis functions
│ │ └── headlines_analyzer/
│ ├── collectors/ # Data collection functions
│ │ └── headline_collector/
│ ├── parsers/ # Data parsing functions
│ │ ├── cnn/
│ │ └── liga/
│ ├── requirements.in # Python dependencies source
│ └── requirements.txt # Compiled Python dependencies
└── shared_tools/ # Common utilities
├── headline_analyzer.py
└── s3_helper.py


## Prerequisites
- AWS CLI configured with appropriate credentials
- Terraform installed
- Python 3.x
- pip-tools (for managing Python dependencies)
- Make

## Setup and Deployment

### 1. Build Lambda Layers
```bash
make build-layers
```
This command:
- Compiles Python requirements
- Creates a Lambda layer with all dependencies

### 2. Prepare Lambda Functions
```bash
make prepare-lambdas
```
This command:
- Packages all Lambda functions (parsers, collectors, analyzers)
- Includes shared tools in each package
- Creates deployment-ready ZIP files

### 3. Deploy Infrastructure
```bash
# Initialize Terraform
make terraform-init

# Plan deployment
make terraform-plan

# Apply changes
make terraform-apply
```

### Cleanup
To remove all created resources:
```bash
make terraform-destroy
```

To clean up local build artifacts:
```bash
make clean
```

## Infrastructure Components
- AWS Lambda Functions
  - Collectors: Data gathering functions
  - Parsers: Data transformation functions
  - Analyzers: Text analysis functions
- S3 Buckets for data storage
- EventBridge/CloudWatch for scheduling
- IAM roles and policies
- [Other AWS services configured in Terraform]

## Development

### Adding New Lambda Functions
1. Create a new directory in the appropriate category (collectors/parsers/analyzers)
2. Add your Python function code
3. Update requirements.in if new dependencies are needed
4. Run `make prepare-lambdas` to package

### Updating Dependencies
1. Modify `lambda_functions/requirements.in`
2. Run `make build-layers` to rebuild the Lambda layer

## Maintenance
- Monitor AWS CloudWatch logs for Lambda execution
- Check S3 bucket contents for data processing results
- Review EventBridge schedules for task timing

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
