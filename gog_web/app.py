import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, render_template
from gog_core.content_generator import generate_content, save_gog_file
from gog_core.gog_parser import parse_gog_file
from gog_core.prompt_formatter import format_prompt  # ✅ INCLUDED
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    content = {"generated": False, "value": ""}
    meta = {}
    prompt = {}
    render = {}

    if request.method == 'POST':
        action = request.form.get("action")

        if action == "upload":
            file = request.files.get("file")
            if file:
                filepath = os.path.join("uploaded.gog")
                file.save(filepath)
                data = parse_gog_file(filepath)
                content = data.get("content", content)
                meta = data.get("meta", {})
                prompt = data.get("prompt", {})
                render = data.get("render", {})

        elif action == "regenerate":
            meta = {
                "title": request.form.get("meta_title", ""),
                "author": request.form.get("meta_author", ""),
                "created": request.form.get("meta_created", ""),
                "gpt_engine": request.form.get("meta_gpt_engine", "gpt-3.5-turbo")
            }

            prompt = {
                "audience": request.form.get("prompt_audience", ""),
                "tone": request.form.get("prompt_tone", ""),
                "format": request.form.get("prompt_format", ""),
                "context": request.form.get("prompt_context", "")
            }

            render = {
                "font": request.form.get("render_font", ""),
                "font_size": request.form.get("render_font_size", ""),
                "layout": request.form.get("render_layout", ""),
                "margin": request.form.get("render_margin", ""),
                "include_headings": "render_include_headings" in request.form
            }

            gog_dict = {
                "meta": meta,
                "prompt": prompt,
                "render": render,
                "content": {"generated": False, "value": ""}
            }

            prompt_text = format_prompt(meta, prompt, render)
            result = generate_content(api_key, {"prompt": prompt_text})
            gog_dict["content"] = {"generated": True, "value": result}

            save_gog_file("generated.gog", gog_dict)
            content = gog_dict["content"]

        elif action == "download":
            # You can trigger a download later via send_file
            pass

    return render_template("index.html", meta=meta, prompt=prompt, render=render, content=content)
