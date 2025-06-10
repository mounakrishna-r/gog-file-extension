import os
import yaml
from jsonschema import validate, ValidationError

def load_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def load_schema(schema_path="gog_schema.yaml"):
    with open(schema_path, "r") as f:
        return yaml.safe_load(f)

def validate_gog_file(file_path: str, schema_path: str = "gog_schema.yaml") -> bool:
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    try:
        gog_data = load_yaml(file_path)
        schema = load_schema(schema_path)

        validate(instance=gog_data, schema=schema)
        print(f"✅ VALID: {file_path} follows GOG schema")
        return True
    except ValidationError as ve:
        print(f"❌ INVALID: {file_path} failed schema validation")
        print(f"Schema Error: {ve.message}")
        return False
    except Exception as e:
        print(f"❌ ERROR while validating {file_path}")
        print(f"Exception: {str(e)}")
        return False