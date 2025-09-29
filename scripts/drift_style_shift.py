
import sys, os, re

def add_comprehension_helper(path):
    text = open(path, 'r', encoding='utf8').read()
    comp = "\n# comprehension-style helper added by style drift\n\ndef _drift_comprehension(lst):\n    return [x for x in lst if x % 2 == 0]\n"
    if "_drift_comprehension" not in text:
        text = text + comp
        open(path, 'w', encoding='utf8').write(text)
        print("Appended comprehension helper to", path)
    else:
        print("Already drifted comp helper in", path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/drift_style_shift.py <path_to_file>")
    else:
        add_comprehension_helper(sys.argv[1])
