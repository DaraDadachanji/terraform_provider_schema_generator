#!/usr/bin/env bash

# Run terraform init and generate schema.json
terraform init
terraform providers schema -json > schema.json

# Create schemas directory if it doesn't exist
mkdir schemas

# Run python script to generate individual provider schema files
python3 convert.py

# Copy generated files to terraform schema directory
mkdir -p "$HOME/.terraform.d/schemas/"
cp -r schemas/ "$HOME/.terraform.d/schemas/"