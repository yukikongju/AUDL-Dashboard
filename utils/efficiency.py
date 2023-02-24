import streamlit as st
import pandas as pd
import itertools

from audl.stats.endpoints.gamestats import GameStats



#  @st.cache
def compute_team_efficiency(game_id, team_ext_id, num_in_pairings, position_radiobox, efficiency_radiobox):
    """ 
    Given game_id, pairings

    Parameters
    ----------
    game_id: str
    num_in_pairings: int
        groupings between 1 and 4: single, duos, trios, quatuors
    """
    game = GameStats(game_id)
    points = game.get_lineup_by_points()
    df_game_players = game.get_players_metadata()

    lineup_dict = {} # key: 12346, value: [134, 1346, 1325]
    lineups = {} # key: [...]: {'offense_win', 'offense_loss', 'offense_incomplete', 'defense_win', 'defense_loss', 'defense_incomplete'}

    # compute pairings results for each point
    for point in points:
        # get lineup
        lineup = point['lineup_offense'] if point['offense'] == team_ext_id else point['lineup_defense']

        # get win/loss/incomplete
        outcome = _get_point_outcome(team_ext_id, point['outcome'])

        # lineup value key dict
        result_key = f'offense_{outcome}' if point['offense'] == team_ext_id else f'defense_{outcome}'

        # for each combination, increment win/loss
        lineup.sort()
        combinations = list(itertools.combinations(lineup, r=num_in_pairings))
        for pairs in combinations:
            pairs_hash = ''.join([str(pid) for pid in pairs])
            if pairs_hash in lineups:
                updated_result = lineups.get(pairs_hash)
                updated_result[result_key] += 1
                lineups[pairs_hash] = updated_result
            else:
                lineup_dict[pairs_hash] = pairs
                result_dict = {
                        'offense_win': 0,
                        'offense_loss': 0,
                        'offense_incomplete': 0,
                        'defense_win': 0,
                        'defense_loss': 0,
                        'defense_incomplete': 0}
                result_dict[result_key] += 1
                lineups[pairs_hash] = result_dict

    # make data frame
    df_lineup = pd.DataFrame.from_dict(lineups, orient='index')

    # compute off and def percentage, original lineup, pairs full name
    offensive_percentages, defensive_percentages, original_ids = [], [], []
    all_full_names = []
    for index, row in df_lineup.iterrows():
        offensive_percentages.append(row['offense_win'] / (row['offense_win'] + row['offense_loss'] + row['offense_incomplete']))
        defensive_percentages.append(row['defense_win'] / (row['defense_win'] + row['defense_loss'] + row['defense_incomplete']))
        pair_ids = lineup_dict.get(index)
        original_ids.append(pair_ids)

        # full name
        full_names = [get_player_full_name_from_id(df_game_players, pid) for pid in pair_ids]
        all_full_names.append(full_names)

    df_lineup['offense_perc'] = offensive_percentages
    df_lineup['defense_perc'] = defensive_percentages
    df_lineup['pairs_id'] = original_ids
    df_lineup['full_name'] = all_full_names

    # sort by
    sorting_key = _get_sorting_key(position_radiobox, efficiency_radiobox)
    df_lineup = df_lineup.sort_values(by=sorting_key, ascending=False).reset_index(drop=True)

    # print
    #  columns_to_keep = ['full_name', sorting_key]
    columns_to_keep = [sorting_key, 'full_name']
    df_lineup = df_lineup[columns_to_keep]

    return df_lineup
    
def _get_sorting_key(position_radiobox, efficiency_radiobox):
    if position_radiobox == 'Offense' and efficiency_radiobox == 'Count':
        sorting_key = 'offense_win'
    elif position_radiobox == 'Offense' and efficiency_radiobox == 'Percentage':
        sorting_key = 'offense_perc'
    elif position_radiobox == 'Defense' and efficiency_radiobox == 'Count':
        sorting_key = 'defense_win'
    elif position_radiobox == 'Defense' and efficiency_radiobox == 'Percentage':
        sorting_key = 'defense_perc'
    return sorting_key
    
def _get_point_outcome(outcome, team_ext_id):
    if outcome == 'incomplete':
        outcome_string = 'incomplete'
    elif outcome == team_ext_id:
        outcome_string = 'win'
    else:
        outcome_string = 'loss'
    return outcome_string


def get_player_full_name_from_id(df_game_players, player_id):
    first_name = df_game_players.loc[df_game_players['id'] == player_id, 'player.first_name'].values[0]
    last_name = df_game_players.loc[df_game_players['id'] == player_id, 'player.last_name'].values[0]
    full_name = ' '.join([first_name, last_name])
    return full_name


