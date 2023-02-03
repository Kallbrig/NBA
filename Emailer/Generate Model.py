import pandas as pd
import numpy as np
from datetime import datetime,date
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
from sklearn.feature_selection import f_regression,SelectKBest,SelectPercentile,chi2
import joblib

def trim_set(frame):
    return frame[((frame['TRB'] > 2) | (frame['AST'] > 5)) & (frame['PTS'] > 15)]

df = pd.read_csv('train_set_full.csv', index_col=0)




df = df.drop(columns=['STAR', 'DPOY_Rank', 'DPOY_First', 'DPOY_Pts Won', 'DPOY_Pts Max', 'DPOY_Share',
                      'DPOY', 'MIP_Rank', 'MIP_First', 'MIP_Pts Won', 'MIP_Pts Max',
                      'MIP_Share', 'MIP', 'MVP_First', 'MVP_Pts Won',
                      'MVP_Pts Max', 'ROTY_Rank', 'ROTY_First',
                      'ROTY_Pts Won', 'ROTY_Pts Max', 'ROTY_Share', 'ROTY', 'SMOTY_Rank',
                      'SMOTY_First', 'SMOTY_Pts Won', 'SMOTY_Pts Max', 'SMOTY_Share',
                      'SMOTY'], errors='ignore')

df = trim_set(df)

df = df[df['Year'] != date.today().year]







