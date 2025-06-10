import argparse
import os
from cli.main import api_key
from gog_core.schema_validator import validate_gog_file
from gog_core.gog_parser import parse_gog_file
from gog_core.content_generator import generate_content, save_gog_file
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")


def cmd_validate(path):
    result = validate_gog_file(path)
    exit(0 if result else 1)

def cmd_generate(path):
    parsed = parse_gog_file(path)
    if parsed["content"].get("generated"):
        print("Content is already generated, use 'regen' to regenerate")
        return
    print("Generating content...")
    content = generate_content(api_key, parsed)

    if content:
        save_gog_file(path, parsed, content)
        print("Content generated and saved.")

def regen(path):
    parsed = parse_gog_file(path)
    print("Regenerating content...")
    content = generate_content(api_key, parsed)

    if content:
        save_gog_file(path, parsed, content)
        print("Content regenerated and saved.")

def main():
    parser = argparse.ArgumentParser(prog="gog-cli", description="GOG file utility")
    subparsers = parser.add_subparsers(dest="command")

    #validate
    validate_parser = subparsers.add_parser("validate", help='Validate a GOG file')
    validate_parser.add_argument("file", help="Path to .gog file")

    #generate
    generate_parser = subparsers.add_parser("generate", help ='generate content for .gog file')
    generate_parser.add_argument("file", help='Path to .gog file')

    #regen
    regen_parser = subparsers.add_parser("regen", help ='Force regenerate content for .gog file')
    regen_parser.add_argument("file", help='Path to .gog file')

    args = parser.parse_args()

    if args.command == "validate":
        cmd_validate(args.file)
    elif args.command == "generate":
        cmd_generate(args.file)
    elif args.command == "regen":
        regen(args.file)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()