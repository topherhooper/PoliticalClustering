import pandas as pd
from core.auth import get_candidates, run_api_query, search_committee, search_candidates

x_column_name = "candidate_id"

def cluster_n_candidates_pandas():
    pd.pivot_table(df, 
    values='D', 
    index=['A', 'B'],
    columns=['C'],)

def get_candidates_df():
    results = get_candidates()
    return pd.DataFrame(results)

def transform_df():
    X = pd.DataFrame(np.ones((5, 2)))
    y = pd.DataFrame(np.ones((5,)))

    X = np.array(X)
    y = np.array(y).squeeze()

def kmeans():
    from sklearn.cluster import KMeans
    import numpy as np
    X = np.array([[1, 2], [1, 4], [1, 0],
                [10, 2], [10, 4], [10, 0]])
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    kmeans.labels_

    kmeans.predict([[0, 0], [12, 3]])

    kmeans.cluster_centers_


if __name__ == "__main__":
    df1 = cluster_n_candidates_pandas()