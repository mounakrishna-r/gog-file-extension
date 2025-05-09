import yaml

def parse_gog_file(path):
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    return {
        "meta": data.get('meta', {}),
        "prompt": data.get('prompt', {}),
        "render": data.get('render', {}),
        "content": data.get('content', {})
    }
