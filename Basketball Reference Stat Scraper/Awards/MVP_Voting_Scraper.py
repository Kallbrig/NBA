"""
This file will scrape a single year's MVP data.
Args:
year - Pretty self-explanatory
data_dir - Required so that if the file already exists, it won't be pulled again. Prevents rate limit hits.
"""

import os
from time import sleep

import pandas as pd
import requests


def remove_multi_index(df: pd.DataFrame):
    return [i[1] for i in df.columns]


def getdata(url):
    return requests.get(url).text


def scrape_single_year_mvp(year: int, data_dir: str):
    if os.path.exists(os.path.join(data_dir, f'{year}_MVP.csv')):
        print(f"{year} already exists, returning the file.")
        return pd.read_csv(os.path.join(data_dir, f'{year}_MVP.csv'))

    scraped_html = getdata(f"https://www.basketball-reference.com/awards/awards_{year}.html")

    while 'The owner of this website (www.basketball-reference.com) has banned you temporarily from accessing this website' in scraped_html:
        print("You've been temporarily banned from accessing basketball reference.\nSleeping 1 hour then continuing.")
        sleep(3600)
        scraped_html = getdata(f"https://www.basketball-reference.com/awards/awards_{year}.html")

    table = pd.read_html(scraped_html)

    mvp = table[0]
    mvp.columns = remove_multi_index(mvp)
    mvp['Year'] = year
    return mvp


if __name__ == '__main__':
    working_dir = 'MVP'
    print(working_dir)
    for year in range(1980, 2024):
        df = scrape_single_year_mvp(year, working_dir)
        df = df.loc[:, ['Player', 'Age', 'Tm', 'First', 'Pts Won', 'Pts Max', 'Share', 'Year']]
        df.to_csv(os.path.join(working_dir, f'{year}_MVP.csv'))
        print(f'{year} Complete')
