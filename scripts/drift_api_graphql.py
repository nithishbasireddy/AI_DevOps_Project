import sys, os

def migrate_requests_to_gql(path):
    text = open(path, 'r', encoding='utf8').read()
    changed = False
    if "requests.get(" in text or "requests.post(" in text:
        text = text.replace("requests.get(", "gql_query(").replace("requests.post(", "gql_query(")
        changed = True
    if "import requests" in text:
        text = text.replace("import requests", "# import requests (migrated)")
        changed = True
    if changed and "def gql_query" not in text:
        text += "\n\ndef gql_query(q):\n    # GraphQL stub added by drift simulation\n    return {'data': None}\n"
    if changed:
        open(path, 'w', encoding='utf8').write(text)
        print("Migrated", path)
    else:
        print("No requests usage in", path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/drift_api_graphql.py <path_to_file>")
    else:
        migrate_requests_to_gql(sys.argv[1])
