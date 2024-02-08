import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectPercentile
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import joblib
import logging
from datetime import datetime

from utility_functions import trim_set

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_nba_season_year(date=None):
    """
    Determines the NBA season year based on a given date.
    If no date is provided, it uses the current date.

    Args:
    date (datetime, optional): The date for which to determine the NBA season year.
                               If None, the current date is used. Defaults to None.

    Returns:
    int: The NBA season year.
    """
    if date is None:
        date = datetime.now()

    current_month = date.month
    current_year = date.year

    # Define the NBA season year
    # If it's October or later, the NBA season year is the next calendar year
    nba_season_year = current_year if current_month < 10 else current_year + 1

    return nba_season_year



def main():
    try:
        current_season_start_year = get_nba_season_year() - 1

        mvp_data_dir = 'Basketball Reference Stat Scraper/Awards/MVP'
        player_data_dir = 'Basketball Reference Stat Scraper/player_stats/'

        # print(os.listdir('../'))

        full_data = [
            pd.merge(
                pd.read_csv(os.path.join(player_data_dir, f'{year}_player_stats.csv'), index_col=0).assign(Player=lambda df: df.Player.str.strip('*')),
                pd.read_csv(os.path.join(mvp_data_dir, f'{year}_MVP.csv'), index_col=0),
                how='left'
            ).fillna(0)
            for year in range(1980, current_season_start_year + 1)
        ]

        train = pd.concat(full_data)
        df = trim_set(train)

        feature_list = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
                        'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PER', 'TS%', '3PAr', 'FTr',
                        'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM',
                        'DBPM', 'BPM', 'VORP']

        x = df[feature_list]
        y = df['Share']

        pipe = Pipeline([
            ('feat_selection', SelectPercentile(percentile=60)),
            ('scaler', MinMaxScaler()),
            ('reg', RandomForestRegressor(n_jobs=-1))
        ])

        pipe.fit(x, y)

        filename = f'Models/MVP/{get_nba_season_year()}/MVP_Predictions_{datetime.now().strftime("%Y%m%d")}.pkl'
        joblib.dump(pipe, filename)

        logging.info("Model training completed and model saved.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
