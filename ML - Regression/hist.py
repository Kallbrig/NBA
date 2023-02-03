import pandas as pd

import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import f_regression, SelectKBest, SelectPercentile, chi2
import joblib


def trim_set(frame):
    return frame[((frame['TRB'] > 2) | (frame['AST'] > 5)) & (frame['PTS'] > 15)]
    # return frame[((frame['TRB'] > 5) | (frame['AST'] > 5)) & (frame['PTS'] > 15) & (frame['Win%'] > .5)]


df = pd.read_csv('train_set_full.csv', index_col=0)

# print(df.columns)

df = df.drop(columns=['STAR', 'DPOY_Rank', 'DPOY_First', 'DPOY_Pts Won', 'DPOY_Pts Max', 'DPOY_Share',
                      'DPOY', 'MIP_Rank', 'MIP_First', 'MIP_Pts Won', 'MIP_Pts Max',
                      'MIP_Share', 'MIP', 'MVP_First', 'MVP_Pts Won',
                      'MVP_Pts Max', 'ROTY_Rank', 'ROTY_First',
                      'ROTY_Pts Won', 'ROTY_Pts Max', 'ROTY_Share', 'ROTY', 'SMOTY_Rank',
                      'SMOTY_First', 'SMOTY_Pts Won', 'SMOTY_Pts Max', 'SMOTY_Share',
                      'SMOTY'], errors='ignore')

df = trim_set(df)

df['MVP_Rank'] = df['MVP_Rank'].astype("int")

for year in range(1998, 2022):
    test_set = df[df['Year'] == year]
    test_set = trim_set(test_set)
    # test_set

    y_test = test_set.loc[:, 'MVP_Share', ]
    # y_test

    train_set = df[df['Year'] != year]
    train_set = trim_set(train_set)

    y_train = df.loc[(df['Year'] != year), 'MVP_Share',]

    feature_list = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA',
                    'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA',
                    'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
                    'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
                    'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
                    'BPM', 'VORP']

    x_train = train_set[feature_list]
    x_test = test_set[feature_list]

    # declare a two step pipeline, explicitly giving names to both steps.
    pipe = Pipeline(

        [('feat_selection', SelectPercentile(percentile=60),), ('scaler', MinMaxScaler()),
         ('reg', RandomForestRegressor())])

    pipe.fit(x_train, y_train)

    y_pred = pipe.predict(X=x_test)

    test_set['pred'] = y_pred
    test_set['pred_scaled'] = MinMaxScaler().fit_transform(y_pred.reshape(-1, 1))
    test_set['pred_rank'] = test_set.pred.rank(ascending=False).astype("int")

    saved = test_set.sort_values('pred_rank', ascending=True).head(10)[
        ['pred_rank', 'MVP_Rank', 'Player', 'G', 'PTS', 'TS%', 'AST', 'TRB', 'STL', 'WS/48', 'pred']].reset_index()

    # correct_list = []
    # for i in range (0,5):
    # print(saved['pred_rank'].iloc[i] != saved['MVP_Rank'].iloc[i])
    i = 0

    print(f"{year}")
    print(f"Predicted - {saved[saved.pred_rank == 1].Player.values[0]}")
    print(f"Actual    - {df.loc[(df.MVP_Rank == 1) & (df.Year == year), 'Player'].values[0]}\n")

    # print(f'{year}\n{saved.loc[i,"Player"]}\nPredicted - {saved.loc[i,"pred_rank"]}\nActual - {saved.loc[i,"MVP_Rank"]}\n')
    # if saved.loc[i,"pred_rank"] == saved.loc[i,"MVP_Rank"]:
    #     correct_list.append(True)
