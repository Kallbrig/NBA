import os
import time
from datetime import datetime
import pandas as pd
import requests


# link for extract html data
def getdata(url):
    r = requests.get(url)
    return r.text


def fetch_player_stats_single_year(year: int):
    per_game_data = getdata(f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html')
    adv_data = getdata(f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html')

    # Checks to see if you've hit the rate limit. Waits an hour if you have.
    while 'The owner of this website (www.basketball-reference.com) has banned you temporarily from accessing this ' \
          'website' in per_game_data or 'The owner of this website (www.basketball-reference.com) has banned you ' \
                                        'temporarily from accessing this website' in adv_data:
        print("You've been temporarily banned from accessing basketball reference.\nSleeping 1 hour then continuing.")
        time.sleep(3600)
        per_game_data = getdata(f'https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html')
        adv_data = getdata(f'https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html')

    df = pd.read_html(per_game_data)[0]
    df_adv = pd.read_html(adv_data)[0]

    df = df.drop(df[df['Player'] == 'Player'].index)

    df_adv = df_adv.drop(df_adv[df_adv['Player'] == 'Player'].index)

    new = pd.merge(df, df_adv, on=['Player', 'Age', 'Tm', 'Pos'])

    player_stats_list = ['Player', 'Pos', 'Age', 'Tm', 'G_x', 'GS', 'MP_x', 'FG', 'FGA',
                         'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
                         'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
                         'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%',
                         'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS',
                         'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']

    player_stats_list_correct = ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
                                 '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
                                 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PER',
                                 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%',
                                 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM',
                                 'VORP']

    # cuts down the columns to what is listed in player_stats_list_correct
    new = new[player_stats_list]
    new.columns = player_stats_list_correct

    # This gets rid of traded players entirely as they have no team stats
    new = new.drop_duplicates(subset='Player', keep=False).reset_index(drop=True)

    # Fills nan's with 0
    new.fillna(value=0, inplace=True)

    # Adds a year column
    new['Year'] = year

    if not os.path.isdir(f'../Data/Test Sets/{datetime.now().strftime("%Y")}'):
        os.mkdir(f'../Data/Test Sets/{datetime.now().strftime("%Y")}')

    new.to_csv(
        f'../Data/Test Sets/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%Y%m%d")}_player_stats.csv')

    new.to_csv(f'../Basketball Reference Stat Scraper/player_stats/{year}_player_stats.csv')

    print(datetime.now().strftime("%m/%d/%Y"), 'Complete')


if __name__ == '__main__':

    # New NBA season starts in October (10)
    if datetime.now().month > 10:
        year = datetime.now().year + 1
    else:
        year = datetime.now().year

    fetch_player_stats_single_year(year)
