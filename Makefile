LAMBDA_DIR = lambda_functions
LAMBDA_PARSERS_DIR=$(LAMBDA_DIR)/parsers
LAMBDA_COLLECTOR_DIR=$(LAMBDA_DIR)/collectors
SHARED_TOOLS=shared_tools
OUTPUT_DIR=lambda_packages
INFRA_DIR=infrastructure

build-layers:
	@echo "Building Lambda layer in the `$(LAMBDA_DIR)` folder"
	cd $(LAMBDA_DIR) && \
	pip-compile requirements.in -o requirements.txt && \
	mkdir -p python && \
	pip install --target python -r requirements.txt && \
	zip -r layer.zip python && \
	rm -rf python



prepare-lambdas: build-layers
	@echo "Preparing Parser Lambda functions..."
	@mkdir -p $(OUTPUT_DIR)
	@cp $(LAMBDA_DIR)/layer.zip $(OUTPUT_DIR)/
	@for lambda in $(LAMBDA_PARSERS_DIR)/*; do \
		if [ -d "$$lambda" ] && [ "$$lambda" != "$(LAMBDA_PARSERS_DIR)/python" ]; then \
			name=$$(basename $$lambda); \
			echo "Packaging Lambda: $$name"; \
			mkdir -p $(OUTPUT_DIR)/$$name; \
			cp -r $$lambda/* $(OUTPUT_DIR)/$$name/; \
			cp -r $(SHARED_TOOLS) $(OUTPUT_DIR)/$$name/; \
			cd $(OUTPUT_DIR)/$$name && zip -r ../$$name.zip . --exclude '*/__pycache__/*'; \
			cd - > /dev/null; \
			rm -rf $(OUTPUT_DIR)/$$name; \
		fi \
	done
	@echo "Packaging for parsers complete!"
	@for lambda in $(LAMBDA_COLLECTOR_DIR)/*; do \
		if [ -d "$$lambda" ] && [ "$$lambda" != "$(LAMBDA_COLLECTOR_DIR)/python" ]; then \
			name=$$(basename $$lambda); \
			echo "Packaging Lambda: $$name"; \
			mkdir -p $(OUTPUT_DIR)/$$name; \
			cp -r $$lambda/* $(OUTPUT_DIR)/$$name/; \
			cp -r $(SHARED_TOOLS) $(OUTPUT_DIR)/$$name/; \
			cd $(OUTPUT_DIR)/$$name && zip -r ../$$name.zip . --exclude '*/__pycache__/*'; \
			cd - > /dev/null; \
			rm -rf $(OUTPUT_DIR)/$$name; \
		fi \
	done
	@echo "Packaging for collectors complete!"
	@echo "Packaging complete!"


terraform-init:
	@echo "Initializing Terraform..."
	cd $(INFRA_DIR) && terraform init

terraform-plan:
	@echo "Planning Terraform deployment..."
	cd $(INFRA_DIR) && terraform plan -out=tfplan

terraform-apply:
	@echo "Applying Terraform deployment..."
	cd $(INFRA_DIR) && terraform apply tfplan

terraform-destroy:
	@echo "Destroying Infrastructure"
	cd $(INFRA_DIR) && terraform destroy

update-lambdas:
	@echo "Updating Lambda functions and layers..."
	cd $(INFRA_DIR) && terraform apply -target=aws_lambda_layer_version.news_parser_layer -target=aws_lambda_function.cnn_parser -target=aws_lambda_function.liga_parser
	@echo "Lambda functions and layers updated!"

clean:
	@echo "Cleaning up..."
	rm -rf $(OUTPUT_DIR)