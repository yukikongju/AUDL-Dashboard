import streamlit as st
import pandas as pd

import utils

from static.parameters import SUPPORTED_SEASONS

st.markdown("# Team Chemistry")




# selectbox: season
season_selectbox = st.selectbox("Season", SUPPORTED_SEASONS)

# computing season calendar
df_calendar = utils.calendar.loading_season_calendar(season_selectbox)

# selectbox: team
team_selectbox = st.selectbox("Team", utils.calendar.get_season_unique_teams(df_calendar))
team_ext_id = utils.calendar.get_team_external_id(df_calendar, team_selectbox)

st.write('### Players Connections')





st.write('### Players Efficiency')

# radiobox: offense/defense efficiency 
efficiency_radiobox = st.radio("Offense/Defense", ['Offense', 'Defense'], horizontal=True)


# radiobox: pairings
pairings_radiobox = st.radio("Pairings", ['Single', 'Duos', 'Trios', 'Quatuors'], horizontal=True)


