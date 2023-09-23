import json
import re


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