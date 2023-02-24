import streamlit as st
import pandas as pd

import utils

from static.parameters import SUPPORTED_SEASONS


#  -----------------------------------------------------------------------

st.markdown("# Team Chemistry")


# selectbox: season
season_selectbox = st.selectbox("Season", SUPPORTED_SEASONS)

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

st.write('### Players Connections')


#  -----------------------------------------------------------------------

st.write('### Players Efficiency')

# radiobox: offense/defense position 
position_radiobox = st.radio("Position", ['Offense', 'Defense'], horizontal=True)

# radiobox: pairings
pairings_dict = {'Single': 1, 'Duos': 2, 'Trios': 3, 'Quatuors': 4}
pairings_radiobox = st.radio("Pairings", pairings_dict.keys(), horizontal=True)
pairing_number = pairings_dict.get(pairings_radiobox)

# radiobox: count/percentage efficiency
efficiency_radiobox = st.radio("Efficiency", ['Count', 'Percentage'], horizontal=True)



# computing players efficiency
for game_id in selected_games:
    df_efficiency = utils.efficiency.compute_team_efficiency(game_id, team_ext_id, pairing_number, position_radiobox, efficiency_radiobox)
    st.write(df_efficiency)

