import os
from datetime import date

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import rcParams
from datetime import datetime


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

matplotlib.use('TKAgg')
#
# sns.set_style('whitegrid')
#
#
# def load_resample_data(directory):
#     try:
#         all_files = os.listdir(directory)
#         all_files.sort()  # Ensures chronological order
#     except FileNotFoundError:
#         print(f"Directory not found: {directory}")
#         return None
#
#     dataframes = []
#     for filename in all_files:
#         try:
#             df = pd.read_csv(f'{directory}/{filename}', index_col=None)
#             df['Date'] = pd.to_datetime(filename[:8])  # Assumes filename starts with date in 'YYYYMMDD' format
#             dataframes.append(df)
#         except Exception as e:
#             print(f"Failed to process file {filename}: {e}")
#
#     if not dataframes:
#         return None
#
#     combined_df = pd.concat(dataframes, axis=0, ignore_index=True)
#     combined_df['Week'] = combined_df['Date'].dt.to_period('W')
#
#     # Group by both Player and Week, then take the last record
#     weekly_resampled_df = combined_df.groupby(['Player', 'Week']).last().reset_index()
#     return weekly_resampled_df
#
#
# # Usage example:
# directory = '2024'
# weekly_data = load_resample_data(directory)
# print(weekly_data.sort_values(['Week', 'Predicted Vote Share'], ascending=[False, True]))
#
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# # Assuming 'weekly_data' is your DataFrame
# # Convert 'Week' back to datetime for plotting
# weekly_data['Week'] = weekly_data['Week'].dt.start_time
#
# # Convert 'Predicted Vote Share' from string to float (e.g., '45%' to 45.0)
# weekly_data['Predicted Vote Share'] = weekly_data['Predicted Vote Share'].str.rstrip('%').astype('float')
#
# # Identify the most recent week
# most_recent_week = weekly_data['Week'].max()
#
# # Determine the top 5 players for the most recent week
# top_5_players = weekly_data[weekly_data['Week'] == most_recent_week].nsmallest(5, 'pred_rank')['Player']
#
# # Filter the DataFrame to include only these top 5 players
# filtered_data = weekly_data[weekly_data['Player'].isin(top_5_players)]
#
# # Plotting
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=filtered_data, x='Week', y='Predicted Vote Share', hue='Player', marker='o')
#
# # Enhancing the plot
# plt.xticks(rotation=45)
# plt.yticks(range(0, 101, 5))  # Setting y-axis ticks from 0 to 100 in increments of 5
# plt.gca().set_yticklabels(['{}%'.format(x) for x in range(0, 101, 5)])  # Add '%' sign back to y-axis labels
# plt.title('Weekly Predicted Vote Shares of Top 5 Players')
# plt.xlabel('Week')
# plt.ylabel('Predicted Vote Share (%)')
# plt.legend(title='Player', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
#
# # Show the plot
#
# plt.show()
#
# # Update font size and bold labels in rcParams
# rcParams.update({'font.size': 12, 'font.weight': 'bold'})
#
# # Assuming 'weekly_data' is your DataFrame
# # Convert 'Week' back to datetime for plotting and handle 'Predicted Vote Share'
# if not pd.api.types.is_datetime64_any_dtype(weekly_data['Week']):
#     weekly_data['Week'] = pd.to_datetime(weekly_data['Week'])
#
# # Convert 'Predicted Vote Share' to strings, then to float (handling None and NaN values)
# weekly_data['Predicted Vote Share'] = weekly_data['Predicted Vote Share'].fillna('0%').astype(str)
# weekly_data['Predicted Vote Share'] = weekly_data['Predicted Vote Share'].str.rstrip('%').astype('float')
#
# # Identify the most recent week
# most_recent_week = weekly_data['Week'].max()
#
# # Filter for the current week
# current_week_data = weekly_data[weekly_data['Week'] == most_recent_week]
#
# # Get the top 10 players based on vote share for the current week
# top_10_current_week = current_week_data.nlargest(10, 'Predicted Vote Share')
#
# # Creating the horizontal bar chart
# plt.figure(figsize=(10, 6))
# ax = sns.barplot(x='Predicted Vote Share', y='Player', data=top_10_current_week, palette='deep', hue='Player',
#                  orient='h')
#
# # Check if legend exists before removing
# if ax.legend_:
#     ax.legend_.remove()
#
# # Adding the text labels on the bars
# for p in ax.patches:
#     width = p.get_width()  # Get the width of the bar
#     plt.text(width + 1,  # Set the horizontal position to just beyond the end of the bar
#              p.get_y() + p.get_height() / 2,  # Set the vertical position to the center of the bar
#              '{:1.1f}%'.format(width),  # Format the label
#              ha='left',  # Align the text to the left
#              va='center',  # Center vertically in the bar
#              fontweight='bold')  # Bold font weight for the label
#
# # Enhancing the plot
# plt.xlim(0, 100)  # Setting x-axis limits from 0 to 100
# plt.title('Top 10 Predicted Vote Shares - Current Week', fontsize=16, fontweight='bold')
# plt.suptitle(f"Date: {most_recent_week.strftime('%Y-%m-%d')}", fontsize=14,
#              fontweight='normal')  # Adding date as subtitle
# plt.xlabel('Predicted Vote Share (%)', fontsize=14, fontweight='bold')
# plt.ylabel('Player', fontsize=14, fontweight='bold')
# plt.tight_layout()
#
# # Show the plot
# plt.show()

def load_and_concatenate_files(directory):
    try:
        all_files = os.listdir(directory)
        all_files.sort()  # Ensures chronological order
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return None

    dataframes = []
    for filename in all_files:
        try:
            df = pd.read_csv(f'{directory}/{filename}', index_col=None)
            df['Date'] = pd.to_datetime(filename[:8])  # Assumes filename starts with date in 'YYYYMMDD' format
            dataframes.append(df)
        except Exception as e:
            print(f"Failed to process file {filename}: {e}")

    return pd.concat(dataframes, axis=0, ignore_index=True) if dataframes else None


def filter_and_resample(frame):
    if frame is None or frame.empty:
        raise ValueError("Input DataFrame is empty or None")

    # Convert 'Predicted Vote Share' to numeric (handling potential '%' characters and NaN values)
    frame['Predicted Vote Share'] = frame['Predicted Vote Share'].str.rstrip('%').astype('float', errors='ignore')

    frame['Week'] = frame['Date'].dt.to_period('W')
    weekly_resampled_df = frame.groupby(['Player', 'Week']).last().reset_index()

    players_to_graph = weekly_resampled_df.loc[(weekly_resampled_df['Date'] == weekly_resampled_df.Date.max()) & (weekly_resampled_df['pred_rank'] <= 5), 'Player'].tolist()
    filtered_frame = weekly_resampled_df[weekly_resampled_df['Player'].isin(players_to_graph)]
    return filtered_frame.sort_values('pred', ascending=False)


def plot_graph(data):
    sns.lineplot(data=data, x='Date', y='pred', hue='Player', marker='o')
    plt.xticks(rotation=45)
    plt.yticks([i / 100 for i in range(0, 101, 5)])
    plt.legend(bbox_to_anchor=(1, 1))
    plt.tight_layout()


def plot_bar_graph(data, most_recent_week):
    current_week_data = data[data['Week'] == most_recent_week]
    top_10_current_week = current_week_data.nlargest(10, 'Predicted Vote Share')

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Predicted Vote Share', y='Player', data=top_10_current_week, palette='deep', hue='Player',
                     orient='h')

    if ax.legend_:
        ax.legend_.remove()

    for p in ax.patches:
        width = p.get_width()
        plt.text(width + 1, p.get_y() + p.get_height() / 2, '{:1.1f}%'.format(width), ha='left', va='center',
                 fontweight='bold')

    plt.xlim(0, 100)
    plt.title('Top 10 Predicted Vote Shares - Current Week', fontsize=16, fontweight='bold')
    plt.suptitle(f"Date: {most_recent_week.strftime('%Y-%m-%d')}", fontsize=14, fontweight='normal')
    plt.xlabel('Predicted Vote Share (%)', fontsize=14, fontweight='bold')
    plt.ylabel('Player', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def save_graph(graph_directory, file_name):
    """
    Save the current matplotlib plot to a specified directory.

    Parameters:
    graph_directory (str): The directory path where the graph will be saved.
    file_name (str): The name of the file to save the graph.

    Returns:
    None

    Raises:
    OSError: If the function fails to create the directory or save the file.
    """
    if not os.path.exists(graph_directory):
        try:
            os.makedirs(graph_directory)
        except OSError as e:
            print(f"Failed to create directory {graph_directory}: {e}")
            return

    try:
        plt.savefig(f'{graph_directory}/{file_name}', dpi=500)
    except OSError as e:
        print(f"Failed to save graph: {e}")

def gen_todays_graph(data_directory, output_directory):
    sns.set_style('whitegrid')
    frame = load_and_concatenate_files(data_directory)

    if frame is None or frame.empty:
        print('Not enough data points to graph yet.')
        return

    filtered_frame = filter_and_resample(frame)
    plot_graph(filtered_frame)

    most_recent_week = filtered_frame['Week'].max()
    plot_bar_graph(filtered_frame, most_recent_week)

    graph_directory = output_directory
    graph_file_name = f'{date.today().strftime("%Y%m%d")}.png'
    save_graph(graph_directory, graph_file_name)


if __name__ == '__main__':
    print(os.getcwd())

    # Paths for the data and output
    data_path = f'../ML - Regression/Historic Predictions/{get_nba_season_year()}'
    output_path = f'../ML - Regression/Historic Predictions/Graphs/{get_nba_season_year()}'

    gen_todays_graph(data_path, output_path)
