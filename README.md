# Terraform Plugin Schemas

The terraform plugin in IntelliJ relies on schemas for providers
to provide suggestions. For community created plugins you have to generate
these schemas yourself. This repository helps you do so

## Instructions

add providers to providers.tf

for example:

```terraform
terraform {
  required_providers {
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "0.71.0"
    }
  }
}
```

then run `run.sh` to generate and move the schemas

## How it works

### Generating providers schema

`terraform init` will find and download required providers

`terraform providers schema` then converts those into a usable json format

### converting providers schema

the raw format of the providers schema is slightly different
from what the plugin expects. `convert.py` fixes the format.

For example the provider blocks look like

```json
 {
    "provider": {
        "version": 0,
        "block": {
            "attributes": {
                "account": {
                    "type": "string",
                    "description": "blah blah blah",
                    "description_kind": "plain",
                    "optional": true
                },
                "browser_auth": {
                    "type": "bool",
                    "description": "blah blah blah",
                    "description_kind": "plain",
                    "optional": true
                }
            }
        }
    }
 }
```

While the plugin expects them to look like:

```json
{
    "provider": {
        "account": {
            "type": "string",
            "description": "blah blah blah",
            "description_kind": "plain",
            "optional": true
        },
        "browser_auth": {
            "type": "bool",
            "description": "blah blah blah",
            "description_kind": "plain",
            "optional": true
        }
    }
}
```

The same is true of the resource schemas and data_source schemas

### Loading the generated schemas

The terraform plugin expects the schemas at `~/.terraform.d/schemas`

You may need to restart IntelliJ for it to take effect

## Extras

`providers.tf` contains a sample for the snowflake plugin

`providers.schema.json` can be used to validate your schema output if you choose to do the conversion some other way
