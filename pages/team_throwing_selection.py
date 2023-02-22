import streamlit as st

from audl.stats.endpoints.seasonschedule import SeasonSchedule

from utils import loading_season_calendar, get_team_games_id, get_season_unique_teams



@st.cache
def get_team_throwing_selection():
    pass
    



st.markdown("# Team Throwing Selection")



# select season
season_selectbox = st.selectbox("Season", [2020, 2021, 2022])
df_calendar = loading_season_calendar(season_selectbox)

# select team
team_selectbox = st.selectbox("Team", get_season_unique_teams(df_calendar))

# select games
games_choices = ['All']
games_choices.extend(get_team_games_id(df_calendar, team_selectbox))
game_selectbox = st.selectbox("Game", games_choices)

# TODO: compute team throwing distribution
if game_selectbox == 'All':
    pass
else:
    pass



#  st.write(df_calendar)

