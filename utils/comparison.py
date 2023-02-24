import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans, OPTICS
from sklearn.mixture import GaussianMixture

from static.parameters import TEAM_STATS_PER_DICT, TEAM_STATS_VS_DICT, PLAYER_STATS_PER_DICT
from audl.stats.endpoints.teamstats import TeamStats
from audl.stats.endpoints.playerstats import PlayerStats


@st.cache_data
def load_team_data(season, per_radiobox, vs_radiobox):
    # convert radiobox inputs
    per = TEAM_STATS_PER_DICT.get(per_radiobox)
    vs = TEAM_STATS_VS_DICT.get(vs_radiobox)

    # fetch table
    table = TeamStats(season, per, vs).get_table()
    return table

@st.cache_data
def get_season_teams(season):
    table = TeamStats(season, 'total', 'team').get_table()
    teams = list(table['teamName'])
    return teams
    
@st.cache_data
def get_team_external_id_from_name(season, team_name):
    table = TeamStats(season, 'total', 'team').get_table()
    team_ext_id = table.loc[table['teamName'] == team_name, 'teamID'].values[0]
    return team_ext_id
    

@st.cache_data
def load_player_data(season, per_radio, team_ext_id): # TODO
    per = PLAYER_STATS_PER_DICT.get(per_radio)
    table = PlayerStats(season, per, team_ext_id).fetch_table()
    return table


@st.cache_data
def plot_comparison(dataset, dimension_reduction_radiobox, cluster_radiobox, comparison_id, comparison_name):
    # remove categorical data and drop NAs
    df_subset = dataset.drop([comparison_id, comparison_name], axis=1)
    df_subset = df_subset.dropna()
    team_names = dataset.dropna()[comparison_name]

    # perform dimension reduction
    model = create_dimension_reduction_model(dimension_reduction_radiobox)
    reductions = model.fit_transform(df_subset)
    df_subset['x'], df_subset['y'] = reductions[:, 0], reductions[:, 1]

    # make clusters
    cluster = create_cluster_model(cluster_radiobox)
    labels = get_cluster_predictions(cluster, df_subset, cluster_radiobox)

    fig = px.scatter(df_subset['x'], df_subset['y'], text=team_names, color=labels)
    return fig

def get_cluster_predictions(cluster, dataset, algorith_name):
    if algorith_name in ['KMeans', 'GaussianMixture']:
        cluster.fit(df_subset)
        labels = cluster.predict(dataset)
    else:
        labels = cluster.fit_predict(dataset)
    return labels


def create_cluster_model(algorithm_name):
    if algorithm_name == 'K-Means':
        model = KMeans(n_clusters=4)
    elif algorithm_name == 'DBSCAN':
        model = DBSCAN(eps=0.3, min_samples=4)
    elif algorithm_name == 'Agglomerative':
        model = AgglomerativeClustering(n_clusters=3)
    elif algorithm_name == 'OPTICS':
        model = OPTICS(eps=0.08, min_samples=6)
    elif algorithm_name == 'Gaussian':
        model = GaussianMixture(n_components=4)
    return model
    
    
def create_dimension_reduction_model(algorithm_name):
    if algorithm_name == 'TSNE':
        model = TSNE(n_components=2, perplexity=5)
    elif algorithm_name == 'PCA':
        model = PCA(n_components=3)
    elif algorithm_name == 'Isomap':
        model = Isomap(n_components=3)
    elif algorithm_name == 'LLE':
        model = LocallyLinearEmbedding(n_components=5)
    return model
    

