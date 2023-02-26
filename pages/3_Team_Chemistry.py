import streamlit as st
import pandas as pd

import utils

from static.parameters import SUPPORTED_SEASONS, CURRENT_SEASON


#  -----------------------------------------------------------------------

st.markdown("# Team Chemistry")


# selectbox: season
season_selectbox = st.selectbox("Season", SUPPORTED_SEASONS, index=SUPPORTED_SEASONS.index(CURRENT_SEASON))

# computing season calendar
df_calendar = utils.calendar.loading_season_calendar(season_selectbox)

# selectbox: team
team_selectbox = st.selectbox("Team", utils.calendar.get_season_unique_teams(df_calendar))
team_ext_id = utils.calendar.get_team_external_id(df_calendar, team_selectbox)

# multiselect: games
all_games_choices = ['All']
games_choices = utils.calendar.get_team_games_id(df_calendar, team_selectbox)
all_games_choices.extend(games_choices)
game_multiselect = st.multiselect("Game", all_games_choices, default='All')

if 'All' in game_multiselect:
    selected_games = games_choices
else:
    selected_games = game_multiselect


#  -----------------------------------------------------------------------

#  st.write('### Players Connections')


#  -----------------------------------------------------------------------

st.write('### Players Efficiency')

# radiobox: pairings
pairings_dict = {'Single': 1, 'Duos': 2, 'Trios': 3, 'Quatuors': 4}
pairings_radiobox = st.radio("Pairings", pairings_dict.keys(), horizontal=True)
pairing_number = pairings_dict.get(pairings_radiobox)


# radiobox: offense/defense position 
position_radiobox = st.radio("Position", ['Offense', 'Defense'], horizontal=True)


# radiobox: count/percentage efficiency
efficiency_radiobox = st.radio("Efficiency", ['Count', 'Percentage'], horizontal=True)


df_concat = utils.efficiency.load_players_efficiency_data(team_ext_id, selected_games, pairing_number)

# sum all pairings off/def wins
df_efficiency = df_concat.groupby(['pairing_hash']).sum().reset_index()

# compute percentage

offensive_percentages, defensive_percentages = [], []
for index, row in df_efficiency.iterrows():
    offensive_percentages.append(round(row['offense_win'] / (row['offense_win'] + row['offense_loss'] + row['offense_incomplete'] + 0.00001), 3))
    defensive_percentages.append(round(row['defense_win'] / (row['defense_win'] + row['defense_loss'] + row['defense_incomplete'] + 0.00001), 3))

df_efficiency['offense_perc'] = offensive_percentages
df_efficiency['defense_perc'] = defensive_percentages

# sort by
sorting_key = utils.efficiency._get_sorting_key(position_radiobox, efficiency_radiobox)
df_efficiency = df_efficiency.sort_values(by=sorting_key, ascending=False).reset_index(drop=True)

# get full name
pairings_names = df_efficiency['pairing_hash'].apply(lambda x: df_concat.loc[df_concat['pairing_hash'] == x, 'full_name'].values[0])
df_efficiency['names'] = pairings_names

# print
columns_to_keep = [sorting_key, 'names']
df_efficiency = df_efficiency[columns_to_keep]

if sorting_key in ['offense_perc', 'defense_perc']:
    st.dataframe(df_efficiency.style.format(subset=[sorting_key], formatter="{:.2f}"))
else:
    st.write(df_efficiency)



