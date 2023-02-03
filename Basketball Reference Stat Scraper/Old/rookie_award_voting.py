from datetime import date

import pandas as pd


def add_pts_share_and_first_share(df):
    # Adds the Pts Share and First Pts Share columns to the df
    # Pts Share is Pts Won / Pts Max. So practically a percentage of Award Points the player won out of the total.
    # First Pts Share is First / Pts Max. This measures the percentage of first place votes out of the total pts
    # available.

    # I thought about doing First / First Pts Avail, but in the early years (1980) voting was one dimensional
    # So that would give players like Magic and Bird a huge advantage because all of their votes were First Votes.

    first = list(df.First)
    pts_won = list(df['Pts Won'])
    pts_max = list(df['Pts Max'])[0]

    pts_share = list()
    first_share = list()

    for i in range(len(first)):
        pts_share.append(round(pts_won[i] / pts_max, 4))
        first_share.append(round(first[i] / pts_max, 4))

    df['Pts Share'] = pts_share
    df['First Pts Share'] = first_share

    return df

def remove_multi_index(df:pd.DataFrame):
    return [i[1] for i in df.columns]


def main():
    for year in range(1980, date.today().year + 1):
        print(year)

        rookies = pd.read_html(f'https://www.basketball-reference.com/awards/awards_{year}.html')[1]

        # Removes Multi-Index from Dataframe because it's not needed
        rookies.columns = remove_multi_index(rookies)

        rookies = add_pts_share_and_first_share(rookies)
        rookies[year] = year

        rookies.to_csv(f'Rookies/{year}_rookies.csv')


if __name__ == '__main__':
    main()
