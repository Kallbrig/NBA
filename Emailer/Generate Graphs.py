import os
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams['savefig.dpi'] = 200

sns.set_style('whitegrid')

all_files = [i for i in os.listdir(f'Historic Predictions/{date.today().year}')]

li = []

for filename in all_files:
    df = pd.read_csv(f'Historic Predictions/{date.today().year}/{filename}', index_col=None, )
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

plt.savefig(f'Historic Predictions/Graphs/{date.today().year}/{filtered_frame.Date.max().strftime("%Y%m%d")}.png',
            dpi=500)
