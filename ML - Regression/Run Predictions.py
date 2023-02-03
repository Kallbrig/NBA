import os
from datetime import datetime

import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def trim_set(frame):
    return frame[((frame['TRB'] > 2) | (frame['AST'] > 5)) & (frame['PTS'] > 15)]


rf_regressor_trained = joblib.load("models/RandomForrestRegressor.pkl", )

test_set = pd.read_csv(
    f'/Users/chaseallbright/Dropbox/NBA/Data/Test Sets/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%Y%m%d")}_player_stats.csv',
    index_col=0)
test_set = trim_set(test_set)

feature_list = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA',
                'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
                'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
                'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
                'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
                'BPM', 'VORP']

x_test = test_set[feature_list]

y_pred = rf_regressor_trained.predict(x_test)

test_set['pred'] = y_pred
test_set['pred_scaled'] = MinMaxScaler().fit_transform(y_pred.reshape(-1, 1))

test_set['pred_rank'] = test_set.pred.rank(ascending=False).astype("int")

saved = test_set.sort_values('pred_rank', ascending=True).head(10)[
    ['pred_rank', 'Player', 'G', 'PTS', 'TS%', 'AST', 'TRB', 'STL', 'BLK', 'OWS', 'DWS', 'WS/48', 'BPM',
     'pred']].set_index('pred_rank')

if not os.path.isdir(f'Historic Predictions/{datetime.now().strftime("%Y")}'):
    os.mkdir(f'Historic Predictions/{datetime.now().strftime("%Y")}')

saved.to_csv(
    f'Historic Predictions/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%Y%m%d")}_MVP_Predictions.csv')
print(test_set.sort_values('pred_rank', ascending=True).head(10)[
          ['pred_rank', 'Player', 'G', 'PTS', 'TS%', 'AST', 'TRB', 'STL', 'BLK', 'OWS', 'DWS', 'WS/48', 'BPM', 'pred']])
