
import os, time, csv, pytest
import reviewer

METRICS_CSV = "metrics.csv"

def ensure_metrics():
    if not os.path.exists(METRICS_CSV):
        with open(METRICS_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp","run_id","repo","test","TP","FP","FN","notes"])

def log_metrics(run_id, repo, test, tp, fp, fn, notes=""):
    ensure_metrics()
    with open(METRICS_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([int(time.time()), run_id, repo, test, tp, fp, fn, notes])

def call_reviewer_and_log(run_id, repo, test_name, diff_text, expected_phrase=None, expect_no_issue=False):
    try:
        output = reviewer.review_code_diff(diff_text)
    except Exception as e:
        log_metrics(run_id, repo, test_name, tp=0, fp=0, fn=1, notes=f"exception:{e}")
        pytest.fail(f"Reviewer crashed: {e}")
    out_lower = output.lower() if isinstance(output, str) else str(output).lower()
    if expected_phrase:
        if expected_phrase.lower() in out_lower:
            log_metrics(run_id, repo, test_name, tp=1, fp=0, fn=0, notes="expected phrase found")
        else:
            log_metrics(run_id, repo, test_name, tp=0, fp=0, fn=1, notes="expected phrase NOT found")
            pytest.fail(f"Expected phrase '{expected_phrase}' not found in reviewer output.")
    elif expect_no_issue:
        if out_lower.strip() and "no immediate suggestions" not in out_lower:
            log_metrics(run_id, repo, test_name, tp=0, fp=1, fn=0, notes="unexpected suggestion")
            pytest.fail("Reviewer produced unexpected suggestions.")
        else:
            log_metrics(run_id, repo, test_name, tp=1, fp=0, fn=0, notes="no suggestion as expected")
    else:
        if out_lower.strip() and "no immediate suggestions" not in out_lower:
            log_metrics(run_id, repo, test_name, tp=1, fp=0, fn=0, notes="general suggestion found")
        else:
            log_metrics(run_id, repo, test_name, tp=0, fp=0, fn=1, notes="no output")
            pytest.fail("Reviewer produced no output (expected suggestion).")

# ---------- Example tests ----------
def test_syntax_context_drift():
    run_id = "drift_syntax_1"
    repo = "modern-repo"
    test_name = "syntax_match_case"
    diff_content = """
--- a/modern-repo/calculator.py
+++ b/modern-repo/calculator.py
@@ -1,6 +1,15 @@
-def add(x, y):
-    return x + y
+def calculate(x, y, operation):
+    match operation:
+        case 'add':
+            return x + y
+        case 'subtract':
+            return x - y
+        case _:
+            return "Invalid operation"
"""
    call_reviewer_and_log(run_id, repo, test_name, diff_content, expected_phrase="match")

def test_simple_bug_detection():
    run_id = "baseline_bug_1"
    repo = "legacy-repo"
    test_name = "off_by_one"
    diff_content = """
--- a/legacy-repo/utils.py
+++ b/legacy-repo/utils.py
@@ -1,6 +1,6 @@
 def sum_first_n(arr, n):
-    s = 0
-    for i in range(n):
-        s += arr[i]
+    s = 0
+    for i in range(n+1):
+        s += arr[i]
     return s
"""
    call_reviewer_and_log(run_id, repo, test_name, diff_content, expected_phrase="off-by-one")

def test_no_false_positive_on_clean_change():
    run_id = "negative_1"
    repo = "legacy-repo"
    test_name = "clean_refactor"
    diff_content = """
--- a/legacy-repo/formatter.py
+++ b/legacy-repo/formatter.py
@@ -1,6 +1,6 @@
 def format_name(first, last):
-    return first + " " + last
+    return f"{first} {last}"
"""
    call_reviewer_and_log(run_id, repo, test_name, diff_content, expect_no_issue=True)
