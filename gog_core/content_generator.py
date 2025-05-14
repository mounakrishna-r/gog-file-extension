from openai import OpenAI
from .prompt_formatter import format_prompt

def generate_content(api_key, full_metadata):
    client = OpenAI(api_key=api_key)
    prompt_text = format_prompt(full_metadata["prompt"])
    engine = full_metadata["meta"].get("gpt_engine", "gpt-3.5-turbo")

    try:
        response = client.chat.completions.create(
            model=engine,
            messages=[
                {"role": "system", "content": "You are an intelligent document generator."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def save_gog_file(path, gog_file):
    with open(path, 'w') as f:
        import yaml
        yaml.dump(gog_file, f, sort_keys=False)
