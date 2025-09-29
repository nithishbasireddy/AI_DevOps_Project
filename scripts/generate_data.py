
import os
os.makedirs("data/baseline", exist_ok=True)
os.makedirs("data/epoch1", exist_ok=True)
os.makedirs("data/epoch2", exist_ok=True)

baseline_snippets = [
("snippet1.py",
"""import requests
def fetch_json(url):
    r = requests.get(url)
    return r.json()
"""),
("snippet2.py",
"""def sum_list(nums):
    s = 0
    for i in range(len(nums)):
        s += nums[i]
    return s
"""),
("snippet3.py",
"""def find_max(arr):
    maximum = arr[0]
    for x in arr:
        if x > maximum:
            maximum = x
    return maximum
"""),
("snippet4.py",
"""import json, os
def load_config(path):
    with open(path) as f:
        cfg = json.load(f)
    return cfg
"""),
("snippet5.py",
"""class Counter:
    def __init__(self):
        self.n = 0
    def add(self, x):
        self.n += x
    def value(self):
        return self.n
"""),
("snippet6.py",
"""def process(data):
    if data == None:
        return []
    if data == []:
        return data
    res = []
    for item in data:
        if item % 2 == 0:
            res.append(item)
    return res
"""),
]

for fname, text in baseline_snippets:
    open(os.path.join("data","baseline",fname), "w", encoding="utf8").write(text)

# epoch1: small drift (replace requests usage with gql_query stub OR add walrus)
for fname, _ in baseline_snippets:
    code = open(os.path.join("data","baseline",fname)).read()
    if "requests" in code:
        code1 = code.replace("requests.get(", "gql_query(").replace("import requests", "# import requests (migrated)")
        code1 += "\n\ndef gql_query(q):\n    return {'data':None}\n"
    else:
        code1 = code + "\n# walrus example\nif (n := 5) > 3:\n    pass\n"
    open(os.path.join("data","epoch1",fname), "w", encoding="utf8").write(code1)

# epoch2: heavier drift - insert match-case helper
for fname, _ in baseline_snippets:
    code = open(os.path.join("data","epoch1",fname)).read()
    helper = "\n# match-case helper added\n\ndef _drift_match_demo(x):\n    match x:\n        case 1:\n            return 'one'\n        case _:\n            return 'other'\n"
    open(os.path.join("data","epoch2",fname), "w", encoding="utf8").write(helper + code)

print("data generated: data/baseline, data/epoch1, data/epoch2")
