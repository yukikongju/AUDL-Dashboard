import streamlit as st
import altair as alt
import matplotlib.pyplot as plt

from audl.stats.endpoints.playerstats import PlayerStats
from audl.stats.endpoints.teamstats import TeamStats
from audl.stats.endpoints.gamestats import GameStats
from audl.stats.endpoints.seasonschedule import SeasonSchedule

from utils import loading_season_calendar, get_season_unique_teams, get_team_games_id
from utils import find_games_id_with_city_abbrev
from plotnine import ggplot, aes, geom_bar

import utils

@st.cache
def load_season_players(season):
    response = PlayerStats(season, 'total', 'all')
    players = response.fetch_table()
    return players


@st.cache
def filter_player_by_team(df_calendar, team_name):
    response = PlayerStats(season, 'total', team_name)
    pass
    

def get_team_id_from_name(team_name):
    team_id = list(df_calendar[df_calendar['awayTeamName'] == team_name]['awayTeamID'].unique())[0]
    return team_id


st.markdown("# Player Throwing Selection")

# select season
season_selectbox = st.selectbox("Season", [2021, 2022])

# filter by team
df_calendar = loading_season_calendar(season_selectbox)
df_players = load_season_players(season_selectbox)
filter_checkbox = st.checkbox("Filter by team")
if filter_checkbox:
    teams = get_season_unique_teams(df_calendar)
    team_selectbox = st.selectbox("Team", teams)
    team_id = get_team_id_from_name(team_selectbox)

    # get players
    df_team_players = PlayerStats(season_selectbox, 'total', team_id).fetch_table()
    team_players = list(df_team_players['name'])
    player_selectbox = st.selectbox("Player", team_players)
    
else:
    players = list(df_players['name'])
    player_selectbox = st.selectbox("Player", players)
    city_abrev = list(df_players[df_players['name'] == player_selectbox]['teams'])[0]
    if ',' in city_abrev:
        city_abrev1, city_abrev2 = city_abrev.split(', ')

# get player_ext_id
player_ext_id = list(df_players[df_players['name'] == player_selectbox]['playerID'])[0]

# select game
all_games_choices = ['All']
if filter_checkbox:
    games_choices = get_team_games_id(df_calendar, team_selectbox)
else:
    if ',' in city_abrev: # FIXME: doesn't work if player is all-stars
        games_choices = find_games_id_with_city_abbrev(df_calendar, city_abrev2)
    else:
        games_choices = find_games_id_with_city_abbrev(df_calendar, city_abrev)

all_games_choices.extend(games_choices)
game_multiselect = st.multiselect("Game", all_games_choices)

go_button = st.button('Go')


# TODO: updated selected games
if go_button:
    if game_multiselect == 'All':
        selected_games = games_choices
    else:
        selected_games = game_multiselect


# fetch players throws selection
for game_id in game_multiselect:
    df_player_throws = utils.compute_player_throwing_selection(game_id, player_ext_id)
    # show 
    st.write('### Player Throwing Dataset')
    st.write(df_player_throws)


###  Dashboard 1: TODO: Throws Distribution (and success rate)

st.write('### Throwing Distribution')

# aggregating throwing distribution
num_throws = int(df_player_throws.shape[0])
df_throws_distribution = df_player_throws.groupby(['throw_type'])['throw_type'].count().reset_index(name='count')
df_throws_distribution['perc'] = df_throws_distribution['count'] / num_throws
st.write(df_throws_distribution)

# TODO: building plot
#  fig, ax = plt.subplots()
#  ax.bar(df_throws_distribution['throw_type'], df_throws_distribution['count'])
#  st.write(fig)


### Dashboard 2: TODO: Top Receivers

st.write('### Top Receivers')

# radio button: 
all_throws_choices = ['All']
throws_choices = list(df_player_throws['throw_type'].unique())
throws_choices = [choice for choice in throws_choices if choice not in ['Throwaway', 'Pull']]
all_throws_choices.extend(throws_choices)
throws_radiobox = st.radio("Throws", all_throws_choices, horizontal=True)

# find top receivers and their full name
if throws_radiobox == 'All':
    df_top_receivers = df_player_throws.groupby(['receiver_id'])['receiver_id'].count().reset_index(name='count')
else:
    df_top_receivers = df_player_throws[df_player_throws['throw_type'] == throws_radiobox].groupby(['receiver_id', 'throw_type'])['throw_type'].count().reset_index(name='count')

df_top_receivers = df_top_receivers.sort_values(by=['count'], ascending=False)
st.write(df_top_receivers)


