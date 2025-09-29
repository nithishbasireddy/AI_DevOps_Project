import json, os
def load_config(path):
    with open(path) as f:
        cfg = json.load(f)
    return cfg

# walrus example
if (n := 5) > 3:
    pass
