import json
import re

"""
Instructions:

1. Create a file called providers.tf and add any providers you want to use
    to the file. For example:
    ```
    terraform {
        required_providers {
            snowflake = {
                source  = "Snowflake-Labs/snowflake"
                version = "0.71.0"
            }
        }
    }
    ```
2. Run `terraform init` to download the providers
3. Run `terraform providers schema -json > schema.json` to get the raw schema
4. Create a folder named "schemas" in the same directory as this script `mkdir schemas`
5. Run this script to convert the raw schema to the format 
    expected by the terraform plugin sdk
6. Create the schemas directory for the terraform plugin 
    `mkdir -p "$HOME/.terraform.d/schemas/"`
7. Copy the generated files to the schemas directory 
    `cp -r schemas/ "$HOME/.terraform.d/schemas/`
"""

def main():
    """
    converts the raw schema to a schema for each provider
    in the format expected by the terraform plugin sdk
    """
    data = _load_data()
    for provider_id, raw_schema in data['provider_schemas']:
        name = _get_provider_name(provider_id)
        schema = _create_provider_schema(
            raw_schema, 
            provider_id=provider_id, 
            provider_name=name
        )
        _write_json(schema, provider_name=name)


def _load_data(schema_file: str = "schema.json"):
    with open(schema_file) as f:
        data = json.load(f)
        return data


def _create_provider_schema(data: dict, provider_name: str) -> dict:
    """converts a schema for a single provider"""
    return {
        ".schema_version": "2",
        ".sdk_type": "terraform-plugin-sdk-v2",
        "name": provider_name,
        "type": "provider",
        "version": "v0.100.0",
        "provider": data['provider']['block']['attributes'],
        "resources": _convert(data['resource_schemas']),
        "data_sources": _convert(data['data_source_schemas'])
    }

def _get_provider_name(url: str) -> str:
    """extracts provider name from url"""
    result = re.search(r'.*\/([^\/]*)$', url)
    return result.group(1)


def _convert(raw: dict) -> dict:
    """converts schema elements to the value of their block.attributes key"""
    converted = {}
    for k, v in raw.items():
        converted[k] = v['block']['attributes']
    return converted


def _write_json(data: dict, provider_name: str):
    with open(f'schemas/{provider_name}.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    main()