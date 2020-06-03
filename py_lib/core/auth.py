import os
import requests
import pandas as pd
import logging
logger = logging.getLogger()

def get_response(query):
    response = requests.get(query)
    return response

def lookup_candidate(api_key, candidate_id):
    query="https://api.open.fec.gov/v1/candidate/{candidate_id}/?sort=name&sort_hide_null=false&sort_null_only=false&sort_nulls_last=false&page=1&api_key=DEMO_KEY&per_page=20".format(
        candidate_id=candidate_id,
        api_key=api_key
    )
    return get_response(query=query)

def get_candidate_committees(api_key, candidate_id,has_raised_funds="true"):
    query = "https://api.open.fec.gov/v1/candidate/{candidate_id}/filings/?sort=-receipt_date&sort_hide_null=false&sort_null_only=false&has_raised_funds={has_raised_funds}&sort_nulls_last=false&page=1&per_page=20&api_key={api_key}".format(
        candidate_id=candidate_id,
        api_key=api_key,
        has_raised_funds=has_raised_funds
    )
    return get_response(query=query)

def search_candidates(api_key, active_status="true"):
    """
    https://api.open.fec.gov/developers#/candidate/get_candidates_
    """
    query = """https://api.open.fec.gov/v1/candidates/?sort=name&sort_hide_null=false&is_active_candidate={active_status}&sort_null_only=false&sort_nulls_last=false&page=1&per_page=20&api_key={api_key}""".format(
        api_key=api_key,
        active_status=active_status
    )
    return get_response(
        query=query
    )

def search_committee(api_key):
    query = "https://api.open.fec.gov/v1/candidates/search/?sort=name&sort_hide_null=false&is_active_candidate=true&sort_null_only=false&sort_nulls_last=false&page=1&per_page=20&api_key={api_key}".format(
        api_key=api_key
    )
    return get_response(
        query=query
    )

def get_committees():
    with open('/bighead/api_data_gov.key') as f:
        api_key = f.read()
        response = search_committee(api_key=api_key)
        return response.json()['results']

def get_candidates():
    with open('/bighead/api_data_gov.key') as f:
        api_key = f.read()
        response = search_candidates(api_key=api_key)
        return response.json()['results']

def run_api_query(query):
    with open('/bighead/api_data_gov.key') as f:
        api_key = f.read()
        query_string = query(api_key=api_key)
        logging.info(query_string)
        response = requests.get(url=query_string)
        logging.info(response)
        return response.json()['results']

def get_filings_query(api_key):
    """
    keys = ["total_disbursements", "committee_id", "candidate_id"]
    """

    return "https://api.open.fec.gov/v1/filings/?sort_nulls_last=false&sort=-receipt_date&sort_hide_null=false&per_page=20&page=1&api_key={api_key}&sort_null_only=false".format(
        api_key=api_key
    )

def get_schedules(api_key):
    path = "/schedules/schedule_a/"
    return "https://api.open.fec.gov/v1{path}?sort=contribution_receipt_date&sort_hide_null=false&per_page=20&api_key={api_key}&sort_null_only=false".format(
        api_key=api_key,
        path=path
    )


def query_df(query):
    return pd.DataFrame(run_api_query(query))

if __name__ == "__main__":
    logger.setLevel(4)
    df = query_df(get_schedules)
    df2 = df[["total_disbursements", "candidate_id", "committee_id"]].copy()
    pdf = df.pivot_table(values=["total_disbursements"], columns=["candidate_id"], index=["committee_id"], dropna=True, aggfunc=len)