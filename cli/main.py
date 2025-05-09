import os
from gog_core.schema_validator import validate_gog_file
from dotenv import load_dotenv
from gog_core.gog_parser import parse_gog_file
from gog_core.content_generator import generate_content, save_gog_file

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file.")

def main():
    path = "tests/test.gog"
    parsed = parse_gog_file(path)

    if parsed["content"].get("generated"):
        print("\n=== Existing Generated Content ===\n")
        print(parsed["content"].get("value", ""))
        return

    print("\n⏳ Generating content...\n")
    content = generate_content(api_key, parsed)

    if content:
        save_gog_file(path, parsed, content)
        print("\n✅ Content generated and saved.\n")
        print("=== Generated Content ===\n")
        print(content)
    else:
        print("❌ Generation failed.")

if __name__ == "__main__":
    main()
    validate_gog_file("tests/tests_valid.gog")
    validate_gog_file("tests/tests_invalid_missing_fields.gog")