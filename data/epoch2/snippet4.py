
# match-case helper added

def _drift_match_demo(x):
    match x:
        case 1:
            return 'one'
        case _:
            return 'other'
import json, os
def load_config(path):
    with open(path) as f:
        cfg = json.load(f)
    return cfg

# walrus example
if (n := 5) > 3:
    pass
