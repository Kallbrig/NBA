# %%
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
import numpy as np

import seaborn as sns
from matplotlib import pyplot as plt

plt.rcdefaults()

df_original = pd.read_csv('Full Dataset.csv', index_col=0)
df = df_original.copy()

for year in range(2000, 2023):
    df = df[(df.GS / df.G > .8) & (df.MP > 10)]

    X = df.drop(columns=['Player', 'Tm', 'MVP_Rank', 'MVP_First', 'MVP_Pts Won', 'MVP_Pts Max', 'MVP_Share', ])

    X_train = X.loc[X['Year_x'] != year, :]
    X_test = X.loc[X['Year_x'] == year, :]
    y_train = df.loc[df['Year_x'] != year, ['MVP_Share']]
    y_test = df.loc[df['Year_x'] == year, ['MVP_Share']]
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    X_train.drop(columns=['Year_x'], inplace=True)
    X_test.drop(columns=['Year_x'], inplace=True)

    print(f'Fitting Random Forest - {year}')

    rfr = RandomForestRegressor()
    rfr.fit(X_train, y_train)

    print(f'Random Forest Fit - {year}')

    pred = pd.DataFrame(rfr.predict(X_test), columns=['Predicted_y'])

    results = pd.DataFrame(np.column_stack((df.loc[X_test.index, ['Player', 'Year_x']], pred, y_test)),
                           columns=['Player', 'Year', 'Pred_MVP', 'Actual_MVP'])

    print(f'Making Graphs - {year}')
    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 8), )
    sns.barplot(x='Pred_MVP', y='Player', data=results.sort_values('Pred_MVP', ascending=False).head(10), ci=False, )
    plt.ylabel('')
    plt.xlabel('Predicted % of MVP Votes')
    plt.title(f'Predicting the {year} NBA MVP')
    plt.xlim(left=0, right=1)
    plt.savefig(f'plots/pred/{year}_predicted_MVP_RandomForest.png')

    sns.set_style('whitegrid')
    plt.figure(figsize=(10, 8), )
    sns.barplot(x='Actual_MVP', y='Player', data=results.sort_values('Actual_MVP', ascending=False).head(10),
                ci=False, )
    plt.ylabel('')
    plt.xlabel('% of MVP Votes Received')
    plt.title(f'{year} NBA MVP Voting')
    plt.xlim(left=0, right=1)
    plt.savefig(f'plots/actual/{year}_MVP_Actual.png')
