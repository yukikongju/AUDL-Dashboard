import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import pandas as pd

from audl.stats.endpoints.playerstats import PlayerStats

#  import utils
from utils.calendar import loading_season_calendar, load_season_players, get_season_unique_teams, get_team_id_from_team_name, get_team_games_id, find_games_id_with_city_abbrev
from utils.throwing import compute_player_throwing_selection, get_heatmap_throws_completion


from static.parameters import SUPPORTED_SEASONS, CURRENT_SEASON


st.markdown("# Player Throwing Selection")

# select season
season_selectbox = st.selectbox("Season", SUPPORTED_SEASONS, index=SUPPORTED_SEASONS.index(CURRENT_SEASON))

# filter by team
df_calendar = loading_season_calendar(season_selectbox)
df_players = load_season_players(season_selectbox)
filter_checkbox = st.checkbox("Filter by team")
if filter_checkbox:
    teams = get_season_unique_teams(df_calendar)
    team_selectbox = st.selectbox("Team", teams)
    team_id = get_team_id_from_team_name(df_calendar, team_selectbox)

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
game_multiselect = st.multiselect("Game", all_games_choices, default='All')

# updated selected games
if 'All' in game_multiselect:
    selected_games = games_choices
else:
    selected_games = game_multiselect


# fetch players throws selection
dfs = []
for game_id in selected_games:
    df_player_throws = compute_player_throwing_selection(game_id, player_ext_id)
    dfs.append(df_player_throws)

# concat dataframes
st.write('### Player Throwing Dataset')
df_player_throws = pd.concat(dfs)
st.write(df_player_throws)

###  Dashboard 1: Throws Distribution (and success rate)

st.write('### Throwing Distribution')

# aggregating throwing distribution
num_throws = int(df_player_throws.shape[0])
df_throws_distribution = df_player_throws.groupby(['throw_type'])['throw_type'].count().reset_index(name='count')
df_throws_distribution['perc'] = df_throws_distribution['count'] / num_throws
df_throws_distribution = df_throws_distribution.sort_values(by='count', ascending=False).reset_index(drop=True)
st.write(df_throws_distribution)

# TODO: building plot
#  fig, ax = plt.subplots()
#  ax.bar(df_throws_distribution['throw_type'], df_throws_distribution['count'])
#  st.write(fig)


### Dashboard 2: Top Receivers

st.write('### Top Receivers')

# radio button: 
all_throws_choices = ['All']
throws_choices = list(df_player_throws['throw_type'].unique())
throws_choices = [choice for choice in throws_choices if choice not in ['Throwaway', 'Pull']]
all_throws_choices.extend(throws_choices)
throws_radiobox = st.radio("Throws", all_throws_choices, horizontal=True)

# find top receivers and their full name
if throws_radiobox == 'All':
    df_top_receivers = df_player_throws.groupby(['receiver_id', 'receiver_full_name'])['receiver_id'].count().reset_index(name='count')
else:
    df_top_receivers = df_player_throws[df_player_throws['throw_type'] == throws_radiobox].groupby(['receiver_id', 'receiver_full_name','throw_type'])['throw_type'].count().reset_index(name='count')

df_top_receivers = df_top_receivers.sort_values(by=['count'], ascending=False).reset_index(drop=True)
st.write(df_top_receivers)

### Dashboard 3: Throw Completion Heatmap 

st.write('### Throw Completion Heatmap')

throws_heatmap_radiobutton = st.radio('Throw Heatmap', all_throws_choices, horizontal=True)


heatmap = get_heatmap_throws_completion(df_player_throws, throws_heatmap_radiobutton)



