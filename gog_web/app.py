from flask import Flask, request, render_template
from gog_core.gog_parser import parse_gog_file
from gog_core.content_generator import generate_content, save_gog_file
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app=Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    content = ""
    meta = {}
    prompt = {}
    filepath = ""

    if request.method == 'POST':
        file = request.files['file']
        filePath = f"uploaded.gog"
        file.save(filePath)

        data = parse_gog_file(filePath)
        meta = data['meta']
        prompt = data['prompt']

    if not data['content'].get('generated'):
        content = generate_content(api_key, data)
        save_gog_file(filepath, data, content)

    else:
        content = data['content']['value']

    render_template("index.html", meta=meta, prompt=prompt, content=content)


    if __name__ == '__main__':
        app.run(debug=True)
