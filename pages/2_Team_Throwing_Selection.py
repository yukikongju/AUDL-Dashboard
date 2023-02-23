import streamlit as st
import pandas as pd

from audl.stats.endpoints.seasonschedule import SeasonSchedule

import utils
from utils import loading_season_calendar, get_team_games_id, get_season_unique_teams

st.markdown("# Team Throwing Selection")

# select season
season_selectbox = st.selectbox("Season", [2021, 2022])
df_calendar = loading_season_calendar(season_selectbox)

# select team and compute team external id
team_selectbox = st.selectbox("Team", get_season_unique_teams(df_calendar))
team_ext_id = utils.get_team_external_id(df_calendar, team_selectbox)
#  st.write(team_ext_id)


# select games
all_games_choices = ['All']
games_choices = get_team_games_id(df_calendar, team_selectbox)
all_games_choices.extend(games_choices)
game_multiselect = st.multiselect("Game", all_games_choices, default='All')


# compute team throwing distribution
if 'All' in game_multiselect:
    selected_games = games_choices
else:
    selected_games = game_multiselect

#  st.write(selected_games)
#  st.write(games_choices)

# compute team throwing dataset
dfs = []
for game_id in selected_games:
    df_throws = utils.compute_team_throwing_selection(game_id, team_ext_id)
    dfs.append(df_throws)
df_throws_concat = pd.concat(dfs)
st.write('### Team Throwing Dataset')
st.write(df_throws_concat)


st.write('### Team Throwing Selection')

num_throws = int(df_throws_concat.shape[0])
df_throws_distribution = df_throws_concat.groupby(['throw_type'])['throw_type'].count().reset_index(name='count')
df_throws_distribution['perc'] = df_throws_distribution['count'] / num_throws
df_throws_distribution = df_throws_distribution.sort_values(by=['count'], ascending=False).reset_index(drop=True)
st.write(df_throws_distribution)


st.write('### Top Throwers/Receivers')

# radio button: thrower/receiver
thrower_receiver_radiobox = st.radio("Thrower/Receiver", ['Thrower', 'Receiver'], horizontal=True)
if thrower_receiver_radiobox == 'Thrower':
    top_thrower_receiver_choice = 'thrower_id'
    top_thrower_receiver_full_name_choice = 'thrower_full_name'
else:
    top_thrower_receiver_choice = 'receiver_id'
    top_thrower_receiver_full_name_choice = 'receiver_full_name'


# radio button: throw_type
all_throws_choices = ['All']
throws_choices = list(df_throws_concat['throw_type'].unique())
if thrower_receiver_radiobox == 'Receiver':
    throws_choices = [choice for choice in throws_choices if choice not in ['Throwaway', 'Pull']]
all_throws_choices.extend(throws_choices)
throws_radiobox = st.radio("Throws", all_throws_choices, horizontal=True)


# show top throwers/receivers
if throws_radiobox == 'All':
    df_top = df_throws_concat.groupby([top_thrower_receiver_choice, top_thrower_receiver_full_name_choice])[top_thrower_receiver_choice].count().reset_index(name='count')
else:
    df_top = df_throws_concat[df_throws_concat['throw_type'] == throws_radiobox].groupby([top_thrower_receiver_choice, top_thrower_receiver_full_name_choice, 'throw_type'])['throw_type'].count().reset_index(name='count')


df_top['perc'] = df_top['count'] / num_throws
df_top = df_top.sort_values(by=['count'], ascending=False).reset_index(drop=True)
st.write(df_top)
