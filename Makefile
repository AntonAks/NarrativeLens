STACK_NAME=narrativelens
BUCKET_NAME=narrativelens-data-$(shell aws sts get-caller-identity --query Account --output text)

.PHONY: build-layer compile-requirements

## 1. Build Layers (Update dependencies & create ZIP)
build-layer:
	cd lambda_functions/parsers/liga
	pip-compile requirements.in -o requirements.txt
	mkdir -p lambda_functions/parsers/liga/python
	pip install --target lambda_functions/parsers/liga/python -r requirements.txt
	zip -r lambda_functions/parsers/liga/layer.zip lambda_functions/parsers/liga/python
	rm -rf lambda_functions/parsers/liga/python

compile-requirements:
	pip-compile --output-file=requirements.txt requirements.in

## 2. Upload Layer to S3
#deploy_layer: build_layer
#	aws s3 cp layer/shared_tools.zip s3://$(BUCKET_NAME)/layers/shared_tools.zip

### 3. Build Lambda ZIP
#build_lambda:
#	cd lambda_functions/parsers/liga && zip -r ../../../liga_parser.zip .
#
### 4. Upload Lambda to S3
#deploy_lambda: build_lambda
#	aws s3 cp liga_parser.zip s3://$(BUCKET_NAME)/lambdas/liga_parser.zip
#
### 5. Deploy all (CloudFormation + Lambdas + Layer)
#deploy_all: deploy_layer deploy_lambda
#	aws cloudformation deploy \
#		--stack-name $(STACK_NAME) \
#		--template-file infrastructure/base_template.yaml \
#		--capabilities CAPABILITY_NAMED_IAM
#
### 6. Delete all (CloudFormation + S3 cleanup)
#delete_all:
#	aws s3 rm s3://$(BUCKET_NAME)/layers/ --recursive
#	aws s3 rm s3://$(BUCKET_NAME)/lambdas/ --recursive
#	aws cloudformation delete-stack --stack-name $(STACK_NAME)
#
### Cleanup local artifacts
#clean:
#	rm -rf layer python shared_tools.zip liga_parser.zip
