import os
import time
from datetime import datetime

import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from send_email import *
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams['savefig.dpi'] = 200

sns.set_style('whitegrid')


def trim_set(frame):
    return frame[((frame['TRB'] > 2) | (frame['AST'] > 5)) & (frame['PTS'] > 15)]


all_files = [i for i in os.listdir(f'../Historic Predictions/{date.today().year}')]

li = []

for filename in all_files:
    df = pd.read_csv(f'../Historic Predictions/{date.today().year}/{filename}', index_col=None, )
    df['Date'] = filename[:8]
    df['Date'] = pd.to_datetime(df['Date'])
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True, )

players_to_graph = frame.loc[(frame['Date'] == frame.Date.max()) & (frame['pred_rank'] <= 5), 'Player'].tolist()
filtered_frame = frame[frame['Player'].isin(players_to_graph)]
sns.lineplot(data=filtered_frame, x='Date', y='pred', hue='Player', marker='o')
plt.xticks(rotation=45)

plt.yticks([i / 100 for i in range(0, 101, 5)])

plt.legend(bbox_to_anchor=(1, 1))

plt.tight_layout()

plt.savefig(f'../Historic Predictions/Graphs/{date.today().year}/{filtered_frame.Date.max().strftime("%Y%m%d")}.png',
            dpi=500)

time.sleep(2)

rf_regressor_trained = joblib.load("../models/RandomForrestRegressor.pkl", )

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

if not os.path.isdir(f'../Historic Predictions/{datetime.now().strftime("%Y")}'):
    os.mkdir(f'../Historic Predictions/{datetime.now().strftime("%Y")}')

saved.to_csv(
    f'../Historic Predictions/{datetime.now().strftime("%Y")}/{datetime.now().strftime("%Y%m%d")}_MVP_Predictions.csv')
# print(test_set.sort_values('pred_rank', ascending=True).head(10)[
#           ['pred_rank', 'Player', 'G', 'PTS', 'TS%', 'AST', 'TRB', 'STL', 'BLK','OWS','DWS', 'WS/48','BPM', 'pred']])

saved.pred = saved.pred * 100
saved.pred = saved.pred.round(1)
saved.pred = saved.pred.astype(str) + '%'

saved['TS%'] = saved['TS%'] * 100
saved['TS%'] = saved['TS%'].round(1)
saved['TS%'] = saved['TS%'].astype(str) + '%'

saved.columns = ['Predicted Vote Share' if i == 'pred' else i for i in saved.columns]

html_table = saved.to_html()

img_html = get_img_to_html(
    f'../Historic Predictions/Graphs/{date.today().year}/{datetime.now().strftime("%Y%m%d")}.png')

email_text = format_email(html_table, img_html)
send_email(email_text)
