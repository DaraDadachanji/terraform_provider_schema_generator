#!/usr/bin/env bash

# Run terraform init and generate schema.json
terraform init
terraform providers schema -json > schema.json

# Run python script to generate individual provider schema files
python3 main.py

# Copy generated files to terraform schema directory
cp -r schemas/ "$HOME/.terraform.d/schemas/