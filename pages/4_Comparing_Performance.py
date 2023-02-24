import streamlit as st
import pandas as pd

import utils

from static.parameters import SUPPORTED_STATS_SEASONS

st.markdown('# Comparing Performance')


# selectbox: season, per, team
season_selectbox = st.selectbox("Season", SUPPORTED_STATS_SEASONS)
season = 'career' if season_selectbox == 'Career' else season_selectbox

# selectbox: player/team
comparison_selectbox = st.selectbox("Comparing", ['Team', 'Player'])

# get teams
all_teams_choices = ['All']
all_season_teams = utils.comparison.get_season_teams(season)
#  st.write(all_season_teams)
#  all_teams_choices = all_teams_choices.extend(all_season_teams)
all_teams_choices = all_season_teams

#  ------------------------------------------------------------------------

if comparison_selectbox == 'Team':
    per_radiobox = st.radio("Per", ['Total', 'Per game'], horizontal=True)
    team_radiobox = st.radio("vs", ['Team', 'Opponent'], horizontal=True)
    df_performance = utils.comparison.load_team_data(season, per_radiobox, team_radiobox)
    st.markdown('### Team Performance Dataset')
else:
    per_radiobox = st.radio("Per", ['Total', 'Per game', 'Per 10 Points', 'Per 10 possessions', 'Per 100 minutes'], horizontal=True)
    team_selectbox = st.selectbox("Team", all_teams_choices)
    team_ext_id = utils.comparison.get_team_external_id_from_name(season, team_selectbox)

    st.markdown('### Player Performance Dataset')
    df_performance = utils.comparison.load_player_data(season, per_radiobox, team_ext_id)

st.write(df_performance)

#  ------------------------------------------------------------------------


if comparison_selectbox == 'Team':
    st.markdown('### Team Comparison')
    comparison_id, comparison_name = 'teamID', 'teamName'
elif comparison_selectbox == 'Player':
    st.markdown('### Player Comparison')
    comparison_id, comparison_name = 'playerID', 'name'

# radiobox: dimension reduction
dimension_reduction_radiobox = st.radio('Dimension Reduction Algorithm', ['TSNE', 'PCA', 'LLE', 'Isomap'], horizontal=True)

# radiobox: Cluster Algorithms
cluster_radiobox = st.radio('Cluster Algorithm', ['K-Means', 'DBSCAN', 'Agglomerative', 'OPTICS', 'Gaussian'], horizontal=True)

fig = utils.comparison.plot_comparison(df_performance, dimension_reduction_radiobox, cluster_radiobox, comparison_id, comparison_name)
st.plotly_chart(fig)
