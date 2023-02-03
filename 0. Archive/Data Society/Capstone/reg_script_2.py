import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn import metrics

from sklearn.preprocessing import StandardScaler, MinMaxScaler

import seaborn as sns

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

sns.set_style('whitegrid')

df = pd.read_csv('Full Dataset.csv', index_col=0)
df_copy = df.copy()

# year = 1987

for year in range(1980, 2023):
    df = pd.read_csv('Full Dataset.csv', index_col=0)
    df_copy = df.copy()

    print(f'Beginning - {year}')

    df.loc[(df['MVP_Share'] != 0), ['MVP_Votes_Bool']] = 1

    df.loc[df['MVP_Votes_Bool'] != 1, ['MVP_Votes_Bool']] = 0
    df.MVP_Votes_Bool = pd.Categorical(df.loc[:, 'MVP_Votes_Bool'])

    reg_feat_list = ['VORP', 'WS', 'BPM', 'PTS', 'PER', 'TOV', 'FT']
    clf_feat_list = ['Pos', 'Age', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P',
                     '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST',
                     'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PER', 'TS%', '3PAr', 'FTr', 'ORB%',
                     'DRB%', 'TRB%', 'AST%', 'STL%', 'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS',
                     'WS', 'WS/48', 'OBPM', 'DBPM', 'BPM', 'VORP']

    train_data = df[(df['Year_x'] != year)].copy()

    X_train_clf = train_data.loc[:, clf_feat_list]
    X_train_reg = train_data.loc[train_data['MVP_Votes_Bool'] == 1, clf_feat_list]
    y_train_clf = train_data.MVP_Votes_Bool
    y_train_reg = train_data.loc[train_data['MVP_Votes_Bool'] == 1, ['MVP_Share']]

    test_data = df[(df['Year_x'] == year)].copy()

    X_test_clf = test_data.loc[:, clf_feat_list]
    X_test_reg = test_data.loc[test_data['MVP_Votes_Bool'] == 1, reg_feat_list]
    y_test_clf = test_data.MVP_Votes_Bool
    y_test_reg = test_data.MVP_Share

    print(f'Predicting - {year}')

    clf = RandomForestClassifier()
    clf.fit(X_train_clf[clf_feat_list], y_train_clf)

    pred = clf.predict(X_test_clf[clf_feat_list])
    clf.score(X_test_clf[clf_feat_list], y_test_clf)

    X_test_clf['pred'] = pred

    X_test_got_votes = X_test_clf[X_test_clf['pred'] == 1]

    reg = RandomForestRegressor()
    reg.fit(X_train_reg, y_train_reg)

    reg_feature_list = ['WS', 'VORP', 'PER', 'BPM', 'USG%', 'TOV', 'PTS', 'FTr', 'PF']

    X_reg_train = df.loc[(df['MVP_Share'] != 0) & (df.Year_x != year), reg_feature_list]
    y_reg_train = df.loc[(df['MVP_Share'] != 0) & (df.Year_x != year), 'MVP_Share']

    # X_reg_test = df.loc[(df['MVP_Share'] != 0) & (df.Year_x == year),reg_feature_list]
    X_reg_test = X_test_got_votes.loc[:, reg_feature_list]

    rf = RandomForestRegressor()
    rf.fit(X_reg_train, y_reg_train)

    rf.predict(X_reg_test)

    pred = pd.DataFrame(rf.predict(X_reg_test), columns=['Predicted_y'])

    results = pd.DataFrame(np.column_stack((df.loc[X_reg_test.index, ['Player', 'Year_x']], pred,)),
                           columns=['Player', 'Year', 'Pred_MVP', ])

    results.Pred_MVP = results.Pred_MVP * 100

    print('Creating Graphs - {}'.format(year))

    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 8), )
    # sns.barplot(x='Pred_MVP',y='Player',data=results.sort_values('Pred_MVP',ascending=False).head(10),ci=False,palette=sns.color_palette("flare",10))
    sns.barplot(x='Pred_MVP', y='Player', data=results.sort_values('Pred_MVP', ascending=False).head(10), ci=False,
                palette=sns.color_palette("flare", 10))
    plt.ylabel('')
    plt.xlabel('Predicted % of MVP Votes')
    plt.title(f'Predicting the {year} NBA MVP')

    sns.color_palette("rocket", as_cmap=True)
    plt.xlim(left=0, right=100)
    plt.subplots_adjust(left=0.2, )

    plt.savefig(f'plots/pred/{year}_predicted_MVP_RandomForest.png', dpi=400)

    actual = df.loc[(df.Year_x == year) & (df.MVP_Share != 0), :]

    actual.MVP_Share = actual.MVP_Share * 100

    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 8), )
    sns.barplot(x='MVP_Share', y='Player', data=actual.sort_values('MVP_Share', ascending=False).head(10), ci=False,
                palette=sns.color_palette("flare", 10))
    plt.ylabel('')
    plt.xlabel('Percentage (%) of MVP Votes Received')
    plt.title(f'{year} NBA MVP Voting')
    plt.xlim(left=0, right=100)
    plt.subplots_adjust(left=0.2, )

    plt.savefig(f'plots/actual/{year}_MVP.png', dpi=400)

warnings.filterwarnings("default", category=FutureWarning)
