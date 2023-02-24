import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.manifold import TSNE, Isomap, LocallyLinearEmbedding
from sklearn.decomposition import PCA

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
    #  st.write(table)
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
def plot_dimension_reduction(dataset, dimension_reduction_radiobox, comparison_id, comparison_name):
    # remove categorical data and drop NAs
    df_subset = dataset.drop([comparison_id, comparison_name], axis=1)
    df_subset = df_subset.dropna()
    team_names = dataset.dropna()[comparison_name]

    if dimension_reduction_radiobox == 'TSNE':
        model = TSNE(n_components=2, perplexity=5)
    elif dimension_reduction_radiobox == 'PCA':
        model = PCA(n_components=3)
    elif dimension_reduction_radiobox == 'Isomap':
        model = Isomap(n_components=3)
    elif dimension_reduction_radiobox == 'LLE':
        model = LocallyLinearEmbedding(n_components=5)

    reductions = model.fit_transform(df_subset)
    df_subset['x'], df_subset['y'] = reductions[:, 0], reductions[:, 1]

    # TODO: make clusters

    #  fig = plt.figure()
    #  sns.scatterplot(data=df_subset, x='x', y='y', hue='y', alpha=0.3)
    fig = px.scatter(df_subset['x'], df_subset['y'], color=team_names)
    return fig
    
