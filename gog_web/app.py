import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, flash, redirect, url_for
from gog_core.content_generator import generate_content, save_gog_file
from gog_core.gog_parser import parse_gog_file
from gog_core.prompt_formatter import format_prompt  # ✅ INCLUDED
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = "super-secret-key"

@app.route('/', methods=['GET', 'POST'])
def home():
    content = {"generated": False, "value": ""}
    meta = {}
    prompt = {}
    render = {}
    gog_dict = {}

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
            prompt_context = request.form.get("prompt_context", "").strip()
            if not prompt_context:
                flash("⚠️ Cannot generate content without a context.")
                return redirect(url_for("home"))

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
                "context": request.form.get("prompt_context", ""),
                "include_headings": "render_include_headings" in request.form
            }

            render = {
                "font": request.form.get("render_font", ""),
                "font_size": request.form.get("render_font_size", ""),
                "layout": request.form.get("render_layout", ""),
                "margin": request.form.get("render_margin", "")
            }

            gog_dict = {
                "meta": meta,
                "prompt": prompt,
                "render": render,
                "content": {"generated": False, "value": ""}
            }

            result = generate_content(api_key, gog_dict)
            gog_dict["content"] = {"generated": True, "value": result}

            content = gog_dict["content"]

        elif action == "download":
            prompt_context = request.form.get("prompt_context", "").strip()
            if not prompt_context:
                flash("⚠️ Cannot generate content without a context.")
                return redirect(url_for("home"))

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
                "context": request.form.get("prompt_context", ""),
                "include_headings": "render_include_headings" in request.form
            }

            render = {
                "font": request.form.get("render_font", ""),
                "font_size": request.form.get("render_font_size", ""),
                "layout": request.form.get("render_layout", ""),
                "margin": request.form.get("render_margin", "")
            }

            content = {
                "generated": request.form.get("generated", "false"),
                "value": request.form.get("generated_content", "")  # 🟡 You must pass this from the HTML as hidden input
            }

            gog_dict = {
                "meta": meta,
                "prompt": prompt,
                "render": render,
                "content": content
            }

            save_gog_file("downloaded.gog", gog_dict)

    return render_template("index.html", meta=meta, prompt=prompt, render=render, content=content)

print("🔥 Flask is starting...")
if __name__ == "__main__":
    app.run(debug=True)