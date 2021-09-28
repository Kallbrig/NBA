import pandas as pd

from sklearn.tree import DecisionTreeRegressor

df = pd.read_csv('../Data/Players With Award Data/complete_players_with_award_voting.csv',index_col = 'Unnamed: 0')

for year in range(1980, 2022):
       print()
       print(year)
       for award in ['MVP','DPOY','ROTY','SMOTY','MIP']:


              df_use = df[[ 'G', 'GS','Year', 'MP', 'FG', 'FGA', 'FG%', '3P',
                     '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
                     'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
                     'Tm_AGE', 'Tm_MOV', 'Tm_SOS',
                     'Tm_SRS', 'Tm_ORtg', 'Tm_DRtg', 'Tm_NRtg', 'Tm_PACE', 'Tm_FTr',
                     'Tm_3PAr', 'Tm_TS%', 'Tm_eFG%',
                     'Tm_Op_eFG%', 'Win%',]]



              X_train = df_use[df_use['Year'] != year].drop('Year',axis=1)
              y_train = df[df['Year'] != year].loc[:,f'{award}_Share']
              # print(len(X_train) == len(y_train))



              X = df_use[df_use['Year'] == year].drop('Year',axis=1)
              y = df[df['Year'] == year].loc[:,f'{award}_Share']
              # print(len(X) == len(y))

              check = df.loc[df['Year'] == year,:].copy()

              # Creating the decision Tree Regressor
              regressor = DecisionTreeRegressor(random_state=0)

              # fit the regressor with X and Y data
              regressor.fit(X_train, y_train)
              try:
                     # Generating Predictions
                     y_pred = regressor.predict(X)
                     # regressor.get_params(deep=True)

                     # Adding predictions to a dataframe so we can check them.
                     check[f'pred_{award}'] = y_pred

                     # Spitting out the players who ranked highest in the predicted voting (Who the computer thinks should win.)
                     check.sort_values(f'pred_{award}',ascending=False)[['Player','Age','G','GS','PTS','AST','TRB','STL','BLK',f'{award}',f'{award}_Rank',f'{award}_Share',f'pred_{award}',]].head(10).to_excel(f'Decision Tree/{year}/{year}_{award}.xlsx')
                     print(award, check.sort_values(f'pred_{award}',ascending=False)[['Player','Age','G','GS','PTS','AST','TRB','STL','BLK',f'{award}',f'{award}_Rank',f'{award}_Share',f'pred_{award}',]].head(1)['Player'].iloc[0])
                     # Spitting out the top actual vote getters from that year. contrast that with the above predictions.
                     # df.loc[df['Year'] == year,['Player','Age','G','GS','PTS','AST','TRB','STL','BLK',f'{award}',f'{award}_Rank',f'{award}_Share',]].sort_values(f'{award}_Share',ascending = False).head(10)

              except:
                     print(f'Can not do {year} {award} predictions.')