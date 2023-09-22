#!/usr/local/Caskroom/miniconda/base/bin/python3

import json

def convert_schema(provider_name):
    data = _load_data()
    provider = _get_provider(data, provider_name=provider_name)
    resources = get_resources(data, provider_name=provider_name)
    data_sources = get_data_sources(data, provider_name=provider_name)

    schema = {
        ".schema_version": "2",
        ".sdk_type": "terraform-plugin-sdk-v2",
        "name": "snowflake",
        "type": "provider",
        "version": "v0.100.0",
        "provider": provider,
        "resources": resources,
        "data_sources": data_sources
    }
    write_json(schema)


def _load_data():
    with open('schema.json') as f:
        data = json.load(f)
        return data


#provider_schemas.snowflake.provider.block.attributes
def _get_provider(data, provider_name):
    provider = data['provider_schemas'][provider_name]['provider']['block']['attributes']
    return provider


#provider_schemas.snowflake.resource_schemas
def get_resources(data, provider_name):
    raw = data['provider_schemas'][provider_name]['resource_schemas']
    return convert(raw)


#provider_schemas.snowflake.data_source_schemas
def get_data_sources(data, provider_name):
    raw = data['provider_schemas'][provider_name]['data_source_schemas']
    return convert(raw)


def convert(raw):
    converted = {}
    for k, v in raw.items():
        converted[k] = v['block']['attributes']
    return converted


def write_json(data):
    with open('output.json', 'w') as f:
        json.dump(data, f, indent=2)
