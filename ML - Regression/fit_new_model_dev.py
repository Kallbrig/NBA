import logging
import os
from datetime import datetime

import joblib
import matplotlib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectPercentile
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from team_mappings import team_mapping
from utility_functions import trim_set

matplotlib.use('Agg')

import matplotlib.pyplot as plt


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
        print(f'Training with data up to {current_season_start_year}')


        mvp_data_dir = '../Basketball Reference Stat Scraper/Awards/MVP'
        player_data_dir = '../Basketball Reference Stat Scraper/player_stats/'
        team_data_dir = '../Basketball Reference Stat Scraper/team_stats/'

        full_data = []
        for year in range(1980, current_season_start_year + 1):
            player_data = pd.read_csv(os.path.join(player_data_dir, f'{year}_player_stats.csv'), index_col=0)

            mvp_data = pd.read_csv(os.path.join(mvp_data_dir, f'{year}_MVP.csv'), index_col=0)
            team_data = pd.read_csv(os.path.join(team_data_dir, f'{year}_tm_stats.csv'), index_col=0)
            team_data.Team = team_data.Team.str.strip('*')

            team_data['Tm'] = team_data.Team.map(team_mapping)


            # Prepend 'Team_' to team data columns except 'Team' and 'Year'
            team_data = team_data.rename(columns={col: f'Team_{col}' for col in team_data.columns if col not in ['Team', 'Year','Tm']})

            # Update team abbreviations in player and mvp data
            for df in [player_data, mvp_data]:
                df['Tm'] = df['Tm'].map(team_mapping).fillna(df['Tm'])

            # Merge player data with mvp data
            merged_data = pd.merge(
                player_data.assign(Player=lambda df: df.Player.str.strip('*')),
                mvp_data,
                how='left'
            ).fillna(0)

            # Merge with team data
            merged_data = pd.merge(
                merged_data,
                team_data,
                left_on=['Tm', 'Year'],
                right_on=['Tm', 'Year'],
                how='left'
            ).fillna(0)

            full_data.append(merged_data)

        train = pd.concat(full_data)
        df = trim_set(train)

        # print(df['Tm'].value_counts())
        # print(df[df.Tm == 0].Team.value_counts())
        feature_list = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
                        'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PER', 'TS%', '3PAr', 'FTr',
                        'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM',
                        'DBPM', 'BPM', 'VORP',

                        'Team_FG', 'Team_FGA', 'Team_FG%',
                        'Team_3P', 'Team_3PA', 'Team_3P%', 'Team_2P', 'Team_2PA', 'Team_2P%',
                        'Team_FT', 'Team_FTA', 'Team_FT%', 'Team_ORB', 'Team_DRB', 'Team_TRB',
                        'Team_AST', 'Team_STL', 'Team_BLK', 'Team_TOV', 'Team_PF', 'Team_PTS',
                        'Team_Age', 'Team_W', 'Team_L', 'Team_MOV', 'Team_SOS', 'Team_SRS',
                        'Team_ORtg', 'Team_DRtg', 'Team_NRtg', 'Team_Pace', 'Team_FTr',
                        'Team_3PAr', 'Team_TS%',

                        ]

        x = df[feature_list]
        y = df['Share']


        pipe = Pipeline([
            ('feat_selection', SelectPercentile(percentile=60)),
            ('scaler', MinMaxScaler()),
            ('reg', RandomForestRegressor(n_jobs=-1))
        ])

        pipe.fit(x, y)
        print(os.getcwd())
        filename = f'../Models/MVP/{get_nba_season_year()}/MVP_Predictions_V2_{datetime.now().strftime("%Y%m%d")}.pkl'
        joblib.dump(pipe, filename)

        logging.info("Model training completed and model saved.")

        import seaborn as sns

        # After fitting the pipeline
        support = pipe.named_steps['feat_selection'].get_support()
        selected_features = [feature for feature, selected in zip(feature_list, support) if selected]

        # Extract feature importances from the fitted model
        feature_importances = pipe.named_steps['reg'].feature_importances_

        # Create a DataFrame with feature names and their importance scores
        importances_df = pd.DataFrame({'Feature': selected_features, 'Importance': feature_importances})

        # Sort the feature importances in descending order
        importances_df = importances_df.sort_values(by='Importance', ascending=False)

        # Plotting using Seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Importance', y='Feature', data=importances_df.head(20))  # Adjust number as needed
        plt.title('Top 20 Feature Importances')
        plt.xlabel('Importance Score')
        plt.ylabel('Features')
        plt.show()


    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
