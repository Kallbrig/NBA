import os
from collections import namedtuple
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from numpy import average


# Scrapes player stats from Basketball reference

def scrape_stats():
    for year in range(1980, int(datetime.now().year + 1)):
        url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(
            year)  # this is the HTML from the given URL

        html = requests.get(url)

        soup = bs(html.text, 'html.parser')

        # use findALL() to get the column headers
        soup.findAll('tr', limit=2)  # use getText()to extract the text we need into a list
        headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll(
            'th')]  # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
        headers = headers[1:]

        # avoid the first header row
        rows = soup.findAll('tr')[1:]
        player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range(len(rows))]

        stats = pd.DataFrame(player_stats, columns=headers)

        stats_df = stats.set_index('Player', drop=True, append=False, )

        stats.to_csv(f'scraped_stats/{year}.csv')

        print(year, 'Scraped')


def convert(dictionary):
    return namedtuple('GenericDict', dictionary.keys())(**dictionary)


def clean_stats(path_to_scraped_stats: str, path_for_cleaned_stats: str):
    try:
        os.chdir(path_to_scraped_stats)
    except:
        print('The Scraped Stats path is invalid.')

    file_list = list(os.walk(os.getcwd()))[0][2]

    # a MacOS workaround.
    try:
        file_list.remove('.DS_Store')
    except:
        pass

    year_list = [int(str(i).split('.')[0]) for i in file_list if 'DS_Store' not in str(i)]

    # creating a list of dataframes containing each year's players
    df_list = []
    for f in file_list:
        df_list.append(pd.read_csv(f, index_col=0, sep=','), )

    # adds the season (year) to the player data
    for i in range(len(df_list)):
        df_list[i]['Year'] = year_list[i]

    # This adds the STAR column to each dataframe and removes the * from the player's name

    player_list = []
    all_star_list = []
    for i in df_list:
        for name in list(i.Player):
            if '*' in str(name):
                all_star_list.append(True)
                player_list.append(str(name).strip('*'))
            else:
                all_star_list.append(False)
                player_list.append(str(name))

        i['STAR'] = all_star_list
        i['Player'] = player_list
        player_list.clear()
        all_star_list.clear()

    # Removes blank entries from the list
    new_df_list = []

    for index in range(len(df_list)):
        e = df_list[index]
        j = e[e.Player != 'nan']
        j = j.reset_index(drop=True)
        new_df_list.append(j)

    df_list = new_df_list

    new_player = dict()
    player_keys = ['Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
                   '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                   'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'STAR', 'Year']

    for i in player_keys:
        new_player[i] = []
    new_list = []
    new_list_copy = []

    for single_year in df_list:

        # Resets the new_player dict to be blank
        for i in player_keys:
            new_player[i] = []

        for i in (single_year.Player.unique()):

            # Identifies which players have been traded by looking at how many entries there were per "Player" or per name.
            if len(single_year[single_year.Player == i]) > 1:

                # Sorts out all seasons by an individual player.
                single_player = single_year[single_year.Player == i]

                # The following line gets rid of the TOT Tm in the player's stats.
                # this information is recalculated below
                # The explanation for this is below.
                single_player = single_player[single_year.Tm != 'TOT']

                # NOTE: THE FOLLOWING INFORMATION IS CORRECT,
                #   BUT
                # I MISUNDERSTOOD HOW PLAYER'S TEAMS WERE BEING REPRESENTED.
                # THIS DOESN'T NEED TO BE CALCULATED MANUALLY, but I still do it.
                # IT'S ALREADY DONE UNDER THE "TOT" TEAM

                # The reason I still calculate it manually is so that team stats can be added at this point. If i
                # used the precalculated TOT stats, the player would not have a unique row for each team they played
                # for.

                #         """
                #         The stats can be divided up into 3 categories:
                #             Static Values are values that won't change regardless
                #                 For example:
                #                             A player's name doesn't change over the course of a season

                #             Sum Values are values that are calculated by adding up all entries
                #                 For example:
                #                             If a player plays 70 games with Team1 and
                #                             12 games with Team2, then total games is calculated
                #                             by sum(70,12) = 82

                #             Weighted Average Values are values that need to be weighted by games played.
                #                 For example:
                #                             if a player took 1 FGA at Team1 over the course of 12 games
                #                             and 3 FGA at Team2 over the course of 70 games
                #                             a simple average(1,3) = 2 FGA isn't correct.
                #         """

                new_player['Player'].append(list(single_player.Player)[0])
                new_player['Pos'].append(list(single_player.Pos)[0])
                new_player['Age'].append(list(single_player.Age)[0])
                new_player['Tm'].append('Traded')
                new_player['STAR'].append(list(single_player.STAR)[0])
                new_player['Year'].append(list(single_player.Year)[0])

                # Sum values are calculated here
                new_player['G'].append(sum(list(single_player.G)))
                new_player['GS'].append(sum(list(single_player.GS)))

                # Weighted average stats are calculated here
                weighted_average_stats = ['MP', 'FG', 'FGA', 'FG%', '3P',
                                          '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                                          'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', ]

                games = list(single_player.G)
                total_games = sum(games)

                weights = [games[i] / total_games for i in range(len(games))]
                for key in weighted_average_stats:
                    item_list = list(single_player[key])
                    avg = round(average(item_list, weights=weights), 2)
                    new_player[key].append(avg)

                # after everything has been calculated, the consolidated player entry is added to the new_list

            else:

                single_player = single_year[single_year.Player == i]

                for key in single_player.keys():
                    new_player[key].append(list(single_player[key])[0])

        # The problem is that new player is mutable.
        # After it's been added to new_list, it is still being changed in the next iteration.
        # so when new_player is cleared at the beginning of the loop, new_player[0-n] is also cleared
        # The solution to this would be to make a non-mutable copy of new_player and add it to new_list,
        # new_list.append(new_player)
    try:
        pd.DataFrame(new_player).to_csv(f'{path_for_cleaned_stats}{new_player["Year"][0]}.csv')
        print(f'{new_player["Year"][0]} Cleaned')
    except:
        print('The Cleaned Stats path is invalid.')


if __name__ == '__main__':
    scrape_stats()
    clean_stats('scraped_stats/', 'cleaned_stats/')
