
import ast, re, random

def detect_unused_imports(code):
    try:
        tree = ast.parse(code)
    except Exception:
        return []
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imported.add(n.asname or n.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported.add(node.module.split(".")[0])
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name):
                used.add(node.value.id)
    unused = [imp for imp in imported if imp and imp not in used]
    return [{"type":"unused_import", "msg":f"Imported '{u}' but not used", "confidence":0.9} for u in unused]

def detect_indexed_loops(code):
    try:
        tree = ast.parse(code)
    except Exception:
        return []
    suggestions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            if isinstance(node.iter, ast.Call) and getattr(node.iter.func, 'id', '') == 'range':
                args = node.iter.args
                if args and isinstance(args[0], ast.Call) and getattr(args[0].func, 'id', '') == 'len':
                    suggestions.append({"type":"use_enumerate", "msg":"Use enumerate() instead of range(len())", "confidence":0.85})
    return suggestions

def detect_eq_none(code):
    matches = re.findall(r"==\s*None", code)
    if matches:
        return [{"type":"eq_none","msg":"Use 'is None' instead of '== None'","confidence":0.8}]
    return []

def detect_requests_usage(code):
    if "requests.get(" in code or "requests.post(" in code or "import requests" in code:
        return [{"type":"requests_usage","msg":"Usage of 'requests' detected (REST). Check for GraphQL migration","confidence":0.7}]
    return []

def detect_long_function(code, threshold=25):
    try:
        tree = ast.parse(code)
    except Exception:
        return []
    suggestions=[]
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                length = node.end_lineno - node.lineno + 1
            else:
                length = max(0, len(code.splitlines()))
            if length > threshold:
                suggestions.append({"type":"long_function","msg":f"Function {node.name} is long ({length} lines)","confidence":0.6})
    return suggestions

def reviewer_review(code):
    suggestions = []
    suggestions.extend(detect_unused_imports(code))
    suggestions.extend(detect_indexed_loops(code))
    suggestions.extend(detect_eq_none(code))
    suggestions.extend(detect_requests_usage(code))
    suggestions.extend(detect_long_function(code))
    for s in suggestions:
        s["confidence"] = min(0.99, max(0.05, s["confidence"] + random.uniform(-0.05, 0.05)))
    return suggestions

def review_code_diff(diff_text):
    # simple heuristic: extract added lines (+ lines in unified diff)
    added_lines = "\n".join([l[1:].rstrip() for l in diff_text.splitlines() if l.startswith("+") and not l.startswith("+++ ")])
    code_to_check = added_lines if added_lines.strip() else diff_text
    sugs = reviewer_review(code_to_check)
    if not sugs:
        return "### Code Review Summary\n\nNo immediate suggestions."
    out = "### Code Review Summary\n\n"
    for s in sugs:
        out += f"- {s['msg']} (confidence {s['confidence']:.2f})\n"
    return out
