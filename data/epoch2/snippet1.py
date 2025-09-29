
# match-case helper added

def _drift_match_demo(x):
    match x:
        case 1:
            return 'one'
        case _:
            return 'other'
# import requests (migrated)
def fetch_json(url):
    r = gql_query(url)
    return r.json()


def gql_query(q):
    return {'data':None}
