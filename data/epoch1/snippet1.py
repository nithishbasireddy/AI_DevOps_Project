# import requests (migrated)
def fetch_json(url):
    r = gql_query(url)
    return r.json()


def gql_query(q):
    return {'data':None}
