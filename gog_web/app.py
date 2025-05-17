import sys
import os
import io
import yaml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, flash, redirect, url_for, send_file
from gog_core.content_generator import generate_content
from gog_core.gog_parser import parse_gog_file
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
                "context": prompt_context,
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

    return render_template(
        'index.html',
        content=content,
        meta=meta,
        prompt=prompt,
        render=render
    )

@app.route('/download', methods=['POST'])
def download():
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
        "generated": bool(request.form.get("content_value")),
        "value": request.form.get("content_value", "")
    }

    gog_dict = {
        "meta": meta,
        "prompt": prompt,
        "render": render,
        "content": content
    }

    gog_file = io.BytesIO()
    yaml.dump(gog_dict, gog_file, allow_unicode=True)
    gog_file.seek(0)

    return send_file(
        gog_file,
        mimetype="application/x-gog",
        as_attachment=True,
        download_name=f"{meta['title'] or 'gog_file'}.gog"
    )

if __name__ == "__main__":
    app.run(debug=True)