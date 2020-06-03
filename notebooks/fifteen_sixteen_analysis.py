import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.decomposition
import scipy.spatial as sp

contribution_colnames = [
    'identification_id',
    'amendment_indicator',
    'report_type',
    'primary-general_indicator',
    'image_number',
    'transaction_type',
    'entity_type',
    'contributor_name',
    'city',
    'state',
    'zip_code',
    'employer',
    'occupation',
    'transaction_date',
    'transaction_amount',
    'other_id',
    'candidate_id',
    'transaction_id',
    'file_id',
    'memo_code',
    'memo_text',
    'fec_record_number'
]

overall_colnames = [
    'CAND_ID', 'CAND_NAME', 'CAND_ICI', 'PTY_CD',
       'CAND_PTY_AFFILIATION', 'TTL_RECEIPTS', 'TRANS_FROM_AUTH',
       'TTL_DISB', 'TRANS_TO_AUTH', 'COH_BOP', 'COH_COP', 'CAND_CONTRIB',
       'CAND_LOANS', 'OTHER_LOANS', 'CAND_LOAN_REPAY', 'OTHER_LOAN_REPAY',
       'DEBTS_OWED_BY', 'TTL_INDIV_CONTRIB', 'CAND_OFFICE_ST',
       'CAND_OFFICE_DISTRICT', 'SPEC_ELECTION', 'PRIM_ELECTION',
       'RUN_ELECTION', 'GEN_ELECTION', 'GEN_ELECTION_PRECENT',
       'OTHER_POL_CMTE_CONTRIB', 'POL_PTY_CONTRIB', 'CVG_END_DT',
       'INDIV_REFUNDS', 'CMTE_REFUNDS'
]


def read_contribution_tables(csv_file):
    return pd.read_csv(
        csv_file, 
        sep='|',
        header=None,
        names=contribution_colnames
        )

def read_candidates_table(csv_file):
    return pd.read_csv(
        csv_file, 
        sep='|', 
        header=None,
        names=overall_colnames
        )

def filter_group_pivot(election_df, race='G2016'):
    filtered_table = election_df[election_df['primary-general_indicator'] == race]
    more_filter = filtered_table.groupby(
        ['candidate_id', 'contributor_name']
    )['transaction_amount'].sum().abs().reset_index()
    return more_filter.pivot_table(
        values='transaction_amount', 
        index='candidate_id', 
        columns='contributor_name'
    )
    
def create_kd_tree(input_df, n_components=10):
    # Non-Negative Matrix Factorization (NMF)
    # https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.NMF.html
    nmf = sklearn.decomposition.NMF(n_components=n_components)

    # fit transform on the pivot matrix, filling nas with zeros
    tst = nmf.fit_transform(input_df.fillna(0))

    # KDTree for fast generalized N-point problems
    # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KDTree.html

    return sp.kdtree.KDTree(tst), tst

def get_id_name_summed(contri_df, candid_df):
    # Contributions
    contributions = contri_df[['candidate_id', 'transaction_amount']]
    contributions = contributions.groupby(['candidate_id',])['transaction_amount'].sum().reset_index()
    # Candidates
    candidate_names = candid_df
    candidate_names = candidate_names[['CAND_ID', 'CAND_NAME']].drop_duplicates()

    # Merge 
    rich_names = pd.merge(contributions, candidate_names, left_on='candidate_id', right_on='CAND_ID')
    rich_names = rich_names.sort_values(by=['transaction_amount'], ascending=False).reset_index(drop=True)
    return rich_names
