def format_prompt(prompt_data):
    context = prompt_data.get("context", "")
    tone = prompt_data.get("tone", "casual")
    audience = prompt_data.get("audience", "general")
    fmt = prompt_data.get("format", "text")

    return (
        f"Write about {context} in a {tone} tone for a {audience} audience in a {fmt} format."
    )