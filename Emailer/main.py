from send_email import *

import os
from datetime import datetime
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from send_email import send_email
from generate_graphs import gen_todays_graph
from utility_functions import get_nba_season_year
from scrape_player_stats import fetch_current_years_stats
from team_mappings import team_mapping
import seaborn as sns
import matplotlib.pyplot as plt

import matplotlib

matplotlib.use('TKAGG')




def plot_top_players_bar_chart(data):
    print("Data type:", type(data))
    print("Data columns:", data.columns)
    print("Data shape:", data.shape)

    sns.set_style('whitegrid')
    sns.set_palette('deep')

    plt.figure(figsize=(10, 6))
    bar_plot = sns.barplot(x='Predicted Vote Share', y='Player', data=data, orient='h')

    plt.xticks([i/10 for i in range(0,11,1)])



    plt.title('Top 10 NBA MVP Candidates')
    plt.tight_layout()
    plt.show()



def trim_set(frame):
    return frame[((frame['TRB'] > 2) | (frame['AST'] > 5)) & (frame['PTS'] > 15)]

def fetch_and_prepare_team_data(year):
    team_data = pd.read_csv(f'../Basketball Reference Stat Scraper/team_stats/{year}_tm_stats.csv', index_col=0)
    team_data['Tm'] = team_data.Team.str.strip('*').map(team_mapping)
    team_data = team_data.rename(columns={col: f'Team_{col}' for col in team_data.columns if col not in ['Team', 'Year', 'Tm']})
    return team_data


def read_and_concatenate_data(dir_path):
    all_files = [i for i in os.listdir(dir_path)]
    li = []
    for filename in all_files:
        df = pd.read_csv(f'{dir_path}/{filename}', index_col=None)
        df['Date'] = filename[:8]
        df['Date'] = pd.to_datetime(df['Date'])
        li.append(df)
    return pd.concat(li, axis=0, ignore_index=True) if li else None


def prepare_and_save_predictions(test_set):
    feature_list = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
                        'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PER', 'TS%', '3PAr', 'FTr',
                        'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM',
                        'DBPM', 'BPM', 'VORP',
                        # ]
                        'Team_FG', 'Team_FGA', 'Team_FG%',
                        'Team_3P', 'Team_3PA', 'Team_3P%', 'Team_2P', 'Team_2PA', 'Team_2P%',
                        'Team_FT', 'Team_FTA', 'Team_FT%', 'Team_ORB', 'Team_DRB', 'Team_TRB',
                        'Team_AST', 'Team_STL', 'Team_BLK', 'Team_TOV', 'Team_PF', 'Team_PTS',
                        'Team_Age', 'Team_W', 'Team_L', 'Team_MOV', 'Team_SOS', 'Team_SRS',
                        'Team_ORtg', 'Team_DRtg', 'Team_NRtg', 'Team_Pace', 'Team_FTr',
                        'Team_3PAr', 'Team_TS%',
                    ]

    # rf_regressor_trained = joblib.load("../ML - Regression/models/MVP_Predictions.pkl")
    rf_regressor_trained = joblib.load(f"../Models/MVP/{get_nba_season_year()}/MVP_Predictions_V2_20240105.pkl")
    x_test = test_set[feature_list]
    y_pred = rf_regressor_trained.predict(x_test)

    test_set['pred'] = y_pred
    test_set['pred_scaled'] = MinMaxScaler().fit_transform(y_pred.reshape(-1, 1))
    test_set['pred_rank'] = test_set['pred'].rank(ascending=False).astype("int")

    saved = test_set.sort_values('pred_rank', ascending=True).head(10)
    saved = saved[
        ['pred_rank', 'Player', 'G', 'PTS', 'TS%', 'AST', 'TRB', 'STL', 'BLK', 'OWS', 'DWS', 'WS/48', 'BPM', 'VORP', 'pred']]
    saved.set_index('pred_rank', inplace=True)

    saved['Predicted Vote Share'] = (saved['pred'] * 100).round(1).astype(str) + '%'
    saved['TS%'] = (saved['TS%'] * 100).round(1).astype(str) + '%'
    saved.columns = ['Predicted Vote Share' if col == 'pred' else col for col in saved.columns]
    saved = saved.loc[:, ~saved.columns.duplicated()]
    saved.to_csv(
        f'../ML - Regression/Historic Predictions/{get_nba_season_year()}/{datetime.now().strftime("%Y%m%d")}_MVP_Predictions.csv')


    return saved



def main():

    output_path = f'../ML - Regression/Historic Predictions/Graphs/{get_nba_season_year()}'


    current_season_year = get_nba_season_year()
    fetch_current_years_stats()

    data_path = f'../ML - Regression/Historic Predictions/{get_nba_season_year()}'

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    frame = read_and_concatenate_data(data_path)
    if frame is None:
        print('Not enough data points to graph yet.')
        return

    gen_todays_graph(data_path, output_path)

    csv_file_path = f'../Data/Test Sets/{current_season_year}/{datetime.now().strftime("%Y%m%d")}_player_stats.csv'
    team_data = fetch_and_prepare_team_data(current_season_year)

    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return

    test_set = pd.read_csv(csv_file_path, index_col=0)
    test_set = trim_set(test_set)
    test_set.reset_index(inplace=True)

    test_set = pd.merge(
        test_set,
        team_data,
        left_on=['Tm', 'Year'],
        right_on=['Tm', 'Year'],
        how='left'
    ).fillna(0)


    saved = prepare_and_save_predictions(test_set)
    plot_top_players_bar_chart(saved)


    html_table = saved.to_html()

    graph_file_path = f'{output_path}/{datetime.now().strftime("%Y%m%d")}.png'
    img_html = get_img_to_html(graph_file_path) if os.path.exists(graph_file_path) else ""

    email_text = format_email(html_table, img_html)
    send_email(email_text)


if __name__ == '__main__':
    main()
