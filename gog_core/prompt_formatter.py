def format_prompt(prompt_data):
    context = prompt_data.get("context", "")
    tone = prompt_data.get("tone", "casual")
    audience = prompt_data.get("audience", "general")
    author = prompt_data.get("author", "general")
    fmt = prompt_data.get("format", "text")
    include_headings = prompt_data.get("include_headings", False)

    return (
        f"Write about {context} in a {tone} tone for a {audience} audience , the audience is like who is hearing it, and author {author} is who is reading, in a {fmt} format.Include headings is {include_headings}"
    )