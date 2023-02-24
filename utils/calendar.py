import streamlit as st
import pandas as pd
import math

from audl.stats.endpoints.seasonschedule import SeasonSchedule
from audl.stats.endpoints.gamestats import GameStats
from audl.stats.endpoints.playerstats import PlayerStats


@st.cache_data
def load_season_players(season):
    response = PlayerStats(season, 'total', 'all')
    players = response.fetch_table()
    return players

@st.cache_data
def loading_season_calendar(season):
    schedule = SeasonSchedule(season)
    calendar = schedule.get_schedule()
    return calendar

@st.cache_data
def get_season_unique_teams(df_calendar):
    teams = list(df_calendar['homeTeamNameRaw'].unique())
    return teams

@st.cache_data
def get_team_id_from_team_name(df_calendar, team_name):
    team_id = list(df_calendar[df_calendar['awayTeamName'] == team_name]['awayTeamID'].unique())[0]
    return team_id

@st.cache_data
def get_team_games_id(df_calendar, team_name):
    tmp = df_calendar[(df_calendar['awayTeamName'] == team_name) | (df_calendar['homeTeamName'] == team_name)]
    games = list(tmp['gameID'])
    return games

@st.cache_data
def find_games_id_with_city_abbrev(df_calendar, city_abrev):
    response = df_calendar[df_calendar['gameID'].str.contains(city_abrev)]
    games_id = list(response['gameID'])
    games_id = list(response['gameID'])
    return games_id
    

@st.cache_data
def get_team_external_id(df_calendar, team_name):
    team_ext_id = df_calendar.loc[df_calendar['homeTeamName'] == team_name, 'homeTeamID'].values[0].strip()
    return team_ext_id

