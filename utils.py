import streamlit as st
import pandas as pd
import math

from audl.stats.endpoints.seasonschedule import SeasonSchedule
from audl.stats.endpoints.gamestats import GameStats

@st.cache
def loading_season_calendar(season):
    schedule = SeasonSchedule(season)
    calendar = schedule.get_schedule()
    return calendar

@st.cache
def get_season_unique_teams(df_calendar):
    teams = list(df_calendar['homeTeamNameRaw'].unique())
    return teams


@st.cache
def get_team_games_id(df_calendar, team_name):
    tmp = df_calendar[(df_calendar['awayTeamName'] == team_name) | (df_calendar['homeTeamName'] == team_name)]
    games = list(tmp['gameID'])
    return games

@st.cache
def find_games_id_with_city_abbrev(df_calendar, city_abrev):
    response = df_calendar[df_calendar['gameID'].str.contains(city_abrev)]
    games_id = list(response['gameID'])
    games_id = list(response['gameID'])
    return games_id
    

def get_throw_type(x1, y1, x2, y2):
    """ 
    get throwing_type: pass, dump, swing, huck, dish
    throw_side: right, left
    """
    # compute angle
    x_delta, y_delta = x2 - x1, y2 - y1
    throw_dist = math.sqrt(x_delta**2 + y_delta**2)
    angle_degrees = math.degrees(math.atan(y_delta / (x_delta + 0.001)))

    # compute throw_type
    threshold_lateral = 15
    threshold_vertical = 40
    if -threshold_lateral <= angle_degrees <= threshold_lateral and y_delta <= 0:
        throw_type = 'Swing'
    elif -threshold_lateral <= angle_degrees <= threshold_lateral and y_delta > 0: 
        throw_type = 'Dish'
    elif y_delta > 40:
        throw_type = 'Huck'
    elif y_delta <= 0 and abs(angle_degrees) > threshold_lateral:
        throw_type = 'Dump'
    else: 
        throw_type = 'Pass'

    # compute throw side
    if angle_degrees >=0 : 
        throw_side = 'Right'
    else:
        throw_side = 'Left'

    # rounding
    signif_number = 3
    x_delta, y_delta = round(x_delta, signif_number), round(y_delta, signif_number)
    throw_dist = round(throw_dist, signif_number)

    return throw_type, throw_side, throw_dist, x_delta, y_delta


def compute_game_events(game_id, tsg_events):
    " helper method "

    output = []
    for res in tsg_events:
        point = res['point']
        events = res['events']
        print(point)

        thrower_id = None
        x_prev, y_prev = None, None
        for event in events:
            t = event['t']
            print(event)
            if t == 3: # pull
                x = event['x']
                y = event['y']
                r_id = int(event['r'])
                dist = round(x**2+y**2, 3) # FIXME: number too big
                row = [game_id, point, r_id, None, 'Pull', dist, x, y] 
                output.append(row)
            if t == 20: # get receiver, throwing_type, x, y
                x = event['x']
                y = event['y']
                r_id = int(event['r'])
                if thrower_id:
                    receiver_id = r_id
                    throw_type, throw_side, throw_distance, x_delta, y_delta = get_throw_type(x_prev, y_prev, x, y)
                    row = [game_id, point, thrower_id, receiver_id, throw_type, throw_distance, x_delta, y_delta]
                    output.append(row)

                # updating thrower
                thrower_id = r_id
                x_prev, y_prev = x, y

            if t == 8: # throwaway
                x = event['x']
                y = event['y']
                throw_type, throw_side, throw_distance, x_delta, y_delta = get_throw_type(x_prev, y_prev, x, y)
                row = [game_id, point, thrower_id, None, 'Throwaway', throw_distance, x_delta, y_delta]
                output.append(row)
                thrower_id = None
            else:
                pass

        print('---')

    columns_names = ['game_id', 'point' ,'thrower_id', 'receiver_id', 'throw_type', 'throw_distance', 'x', 'y']
    df_throws = pd.DataFrame(output, columns=columns_names)
    df_throws['receiver_id'] = df_throws['receiver_id'].astype('Int64')
    return df_throws



@st.cache
def compute_game_throwing_selection(game_id): # HERE
    # get home and away events
    game = GameStats(game_id)
    events_response = game.get_events()
    home_events = events_response['homeEvents']
    away_events = events_response['awayEvents']
    df_game_players = game.get_players_metadata()

    #
    df_home = compute_game_events(game_id, home_events)
    df_away = compute_game_events(game_id, away_events)

    # concat
    df_concat = pd.concat([df_home, df_away])


    # TODO: compute thrower and receiver_name
    #  st.write(df_player_throws)
    #  df_player_throws['receiver_full_name'] = df_player_throws['receiver_id'].apply(lambda x: df_game_players[df_game_players['id'] == x]['player.last_name'].values)
    #  df_player_throws['receiver_full_name'] = df_player_throws['receiver_id'].apply(lambda x: x)


    return df_concat, df_game_players


@st.cache
def compute_player_throwing_selection(game_id, player_ext_id):
    # 
    df_throws, df_game_players = compute_game_throwing_selection(game_id)

    # get player id from external id
    player_id = list(df_game_players[df_game_players['player.ext_player_id'] == player_ext_id]['id'])[0]

    # get player throws
    df_player_throws = df_throws[df_throws['thrower_id'] == player_id]


    return df_player_throws

    
