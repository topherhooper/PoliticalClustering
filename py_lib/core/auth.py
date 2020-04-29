import os
import requests

def hello_world():
    print("hello world.")


def search_candidates(api_key):
    """
    https://api.open.fec.gov/developers#/candidate/get_candidates_
    """
    get_candidates = """https://api.open.fec.gov/v1/candidates/?sort=name&sort_hide_null=false&sort_null_only=false&sort_nulls_last=false&page=1&per_page=20&api_key={api_key}""".format(
        api_key=api_key
    )
    response = requests.get(get_candidates)
    return response

if __name__ == "__main__":
    with open('/bighead/api_data_gov.key') as f:
        api_key = f.read()
        print(search_candidates(api_key=api_key))

