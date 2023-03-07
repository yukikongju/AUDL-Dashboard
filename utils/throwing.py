import streamlit as st
import pandas as pd
import math

from audl.stats.endpoints.seasonschedule import SeasonSchedule
from audl.stats.endpoints.gamestats import GameStats

from static.parameters import THROWS_TYPE_DICT, THROWS_TYPE_DICT_INVERSE


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
                try: 
                    r_id = int(event['r']) # FIXME: investigate why no r sometimes
                    throw_dist = round(math.sqrt(x**2 + y**2), 3)
                    row = [game_id, point, r_id, None, 'Pull', throw_dist, x, y, None, None] 
                    output.append(row)
                except:
                    print('check error')
                    pass
            if t == 20: # get receiver, throwing_type, x, y
                x = event['x']
                y = event['y']
                r_id = int(event['r'])
                if thrower_id:
                    receiver_id = r_id
                    throw_type, throw_side, throw_distance, x_delta, y_delta = get_throw_type(x_prev, y_prev, x, y)
                    row = [game_id, point, thrower_id, receiver_id, throw_type, throw_distance, x_delta, y_delta, x, y]
                    output.append(row)

                # updating thrower
                thrower_id = r_id
                x_prev, y_prev = x, y

            if t == 8: # throwaway
                x = event['x']
                y = event['y']
                throw_type, throw_side, throw_distance, x_delta, y_delta = get_throw_type(x_prev, y_prev, x, y)
                row = [game_id, point, thrower_id, None, 'Throwaway', throw_distance, x_delta, y_delta, x, y]
                output.append(row)
                thrower_id = None
            else:
                pass

        print('---')

    columns_names = ['game_id', 'point' ,'thrower_id', 'receiver_id', 'throw_type', 'throw_distance', 'x', 'y', 'x_field', 'y_field']
    df_throws = pd.DataFrame(output, columns=columns_names)
    df_throws['receiver_id'] = df_throws['receiver_id'].astype('Int64')
    df_throws['thrower_id'] = df_throws['thrower_id'].astype('Int64')
    return df_throws


@st.cache_data
def compute_game_throwing_selection(game_id): 
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
    df_concat['receiver_id'] = df_concat['receiver_id'].astype('Int64')
    df_concat['thrower_id'] = df_concat['thrower_id'].astype('Int64')

    # compute thrower and receiver full names + team external id 
    receivers_full_name = compute_player_full_name_from_id(df_game_players, df_concat['receiver_id'])
    throwers_full_name = compute_player_full_name_from_id(df_game_players, df_concat['thrower_id'])
    team_external_ids = compute_player_column_from_id(df_game_players, df_concat['thrower_id'], 'team')
    receivers_ext_id = compute_player_column_from_id(df_game_players, df_concat['receiver_id'], 'player.ext_player_id')
    throwers_ext_id = compute_player_column_from_id(df_game_players, df_concat['thrower_id'], 'player.ext_player_id')

    #
    df_concat['receiver_full_name'] = receivers_full_name
    df_concat['thrower_full_name'] = throwers_full_name
    df_concat['team_ext_id'] = team_external_ids
    df_concat['receiver_ext_id'] = receivers_ext_id
    df_concat['thrower_ext_id'] = throwers_ext_id

    return df_concat, df_game_players

def compute_player_column_from_id(df_game_players, players_id, column_name):
    team_external_ids = []
    for player_id in players_id:
        try:
            player_id = int(player_id)
            team_id = df_game_players.loc[df_game_players['id'] == player_id, column_name].values[0]
        except:
            team_id = None
        team_external_ids.append(team_id)
    return team_external_ids

def compute_player_full_name_from_id(df_game_players, players_id):
    players_full_name = []
    for player_id in players_id:
        try: 
            player_id = int(player_id)
            first_name = df_game_players.loc[df_game_players['id'] == player_id, 'player.first_name'].values[0]
            last_name = df_game_players.loc[df_game_players['id'] == player_id, 'player.last_name'].values[0]
            full_name = ' '.join([first_name, last_name])
        except:
            full_name = None

        players_full_name.append(full_name)

    return players_full_name

@st.cache_data
def compute_team_throwing_selection(game_id, team_ext_id):
    # compute game throwing selection
    df_throws, df_game_players = compute_game_throwing_selection(game_id)

    # filter by team
    df_team_throws = df_throws[df_throws['team_ext_id'] == team_ext_id]

    return df_team_throws


@st.cache_data
def compute_player_throwing_selection(game_id, player_ext_id):
    # compute game throwing selection
    df_throws, df_game_players = compute_game_throwing_selection(game_id)

    # get player id from external id
    player_id = list(df_game_players[df_game_players['player.ext_player_id'] == player_ext_id]['id'])[0]

    # get player throws
    df_player_throws = df_throws[df_throws['thrower_id'] == player_id]


    return df_player_throws


#  @st.cache_data
def compute_team_throwing_sequence(df_team_throws, sequence_length):
    # remove pulls 
    df_subset = df_team_throws[df_team_throws['throw_type'] != 'Pull']

    # get all throws in points in list
    points_sequences = df_subset.groupby('point')['throw_type'].apply(list)

    # get sequence count
    sequence_count = {}
    for sequence in points_sequences:
        current_sequence = []
        if len(sequence) > sequence_length:
            for throw in sequence[:-sequence_length]:
                throw_hash = str(THROWS_TYPE_DICT.get(throw))
                if len(current_sequence) < sequence_length:
                    current_sequence.append(throw_hash)
                else:
                    # add current sequence to sequence count
                    sequence_hash = ''.join(current_sequence)
                    sequence_count[sequence_hash] = sequence_count.get(sequence_hash, 1) + 1

                    #
                    current_sequence = [throw_hash]
        else: 
            pass

    # sort by value counts
    sorted_counts = sorted(sequence_count.items(), key=lambda x: x[1], reverse=True)

    # convert sequence hash to 
    df_sequence = pd.DataFrame(sorted_counts, columns=['hash', 'count'])
    df_sequence['sequence'] = df_sequence['hash'].apply(lambda x: [THROWS_TYPE_DICT_INVERSE.get(int(i)) for i in x ])
    df_sequence = df_sequence.drop(['hash'], axis=1)

    return df_sequence

