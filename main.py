PROVIDER_NAME = "registry.terraform.io/snowflake-labs/snowflake"
PROVIDER_FRIENDLY_NAME = "snowflake"

from convert import convert_schema
import os

def main():
    create_schema()
    convert_schema(PROVIDER_NAME)
    move_schema()

def create_schema():
    os.system("terraform providers schema -json > schema.json")

def move_schema():
    os.system('mkdir -p "$HOME/.terraform.d/schemas"')
    os.system(f'cp output.json "$HOME/.terraform.d/{PROVIDER_FRIENDLY_NAME}/snowflake.json"')

if __name__ == '__main__':
    main()