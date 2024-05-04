
#
# def load_and_concatenate_files(directory):
#
#     """
#     Load and concatenate CSV files from a specified directory into a single DataFrame.
#
#     Parameters:
#     directory (str): The path to the directory containing CSV files.
#
#     Returns:
#     pandas.DataFrame: A DataFrame containing concatenated data from all CSV files in the directory.
#                       Returns None if the directory is empty or files are not found.
#
#     Raises:
#     FileNotFoundError: If the specified directory does not exist.
#     """
#
#     all_files = os.listdir(directory)
#     dataframes = []
#     for filename in all_files:
#         df = pd.read_csv(f'{directory}/{filename}', index_col=None)
#         df['Date'] = pd.to_datetime(filename[:8])
#         dataframes.append(df)
#     return pd.concat(dataframes, axis=0, ignore_index=True) if dataframes else None
#
# def filter_and_resample(frame):
#     """
#     Filters and resamples a DataFrame to prepare for graph plotting.
#     Specifically, it selects players with a 'pred_rank' less than or equal to 5 on the latest date and
#     resamples the data weekly.
#
#     Parameters:
#     frame (pandas.DataFrame): The DataFrame to be filtered and resampled.
#
#     Returns:
#     pandas.DataFrame: The resampled DataFrame.
#
#     Raises:
#     ValueError: If the input DataFrame is empty or not formatted correctly.
#         """
#
#     players_to_graph = frame.loc[(frame['Date'] == frame.Date.max()) & (frame['pred_rank'] <= 5), 'Player'].tolist()
#     filtered_frame = frame[frame['Player'].isin(players_to_graph)]
#     return filtered_frame.groupby('Player').resample('W', on='Date').agg('last').drop(columns=['Player']).reset_index().sort_values('pred', ascending=False)
#
# def plot_graph(data):
#     """
#     Plots a line graph using seaborn based on the provided DataFrame.
#
#     Parameters:
#     data (pandas.DataFrame): The DataFrame containing the data to plot.
#
#     Returns:
#     None
#
#     Note:
#     This function relies on the current state of matplotlib (plt). Make sure plt is configured correctly before calling.
#     """
#
#     sns.lineplot(data=data, x='Date', y='pred', hue='Player', marker='o')
#     plt.xticks(rotation=45)
#     plt.yticks([i / 100 for i in range(0, 101, 5)])
#     plt.legend(bbox_to_anchor=(1, 1))
#     plt.tight_layout()
#
# def save_graph(graph_directory, file_name):
#     """
#     Save the current matplotlib plot to a specified directory.
#
#     Parameters:
#     graph_directory (str): The directory path where the graph will be saved.
#     file_name (str): The name of the file to save the graph.
#
#     Returns:
#     None
#
#     Raises:
#     OSError: If the function fails to create the directory or save the file.
#     """
#
#     if not os.path.exists(graph_directory):
#         os.makedirs(graph_directory)
#     plt.savefig(f'{graph_directory}/{file_name}', dpi=500)
#
# def gen_todays_graph():
#     """
#     Generates and saves a line graph representing NBA player performance metrics over time.
#     The graph is based on the latest data for players with the highest rankings, aggregated on a weekly basis.
#
#     This function performs the following steps:
#     1. Set the style for seaborn plots.
#     2. Load and concatenate data from CSV files in the specified directory for the current NBA season.
#     3. Filter this data to include only top-ranked players as of the latest date.
#     4. Resample the data on a weekly basis and keep the last record for each week.
#     5. Plot the data using seaborn's lineplot method.
#     6. Save the generated plot to a specified directory as a PNG file.
#
#     The function relies on the utility functions 'get_nba_season_year' to determine the current NBA season year,
#     and other helper functions to load data, filter, resample, plot, and save the graph.
#
#     Parameters:
#     None
#
#     Returns:
#     None
#
#     Raises:
#     FileNotFoundError: If the data files for the current NBA season are not found.
#     OSError: If there is an issue saving the generated plot to a file.
#
#     Note:
#     The function will print a message and exit if there are not enough data points to generate a graph.
#     """
#
#     sns.set_style('whitegrid')
#
#     directory = f'../ML - Regression/Historic Predictions/{get_nba_season_year()}'
#     frame = load_and_concatenate_files(directory)
#
#     if frame is None:
#         print('Not enough data points to graph yet.')
#         return
#
#     filtered_frame = filter_and_resample(frame)
#     plot_graph(filtered_frame)
#
#     graph_directory = f'../ML - Regression/Historic Predictions/Graphs/{get_nba_season_year()}'
#     graph_file_name = f'{date.today().strftime("%Y%m%d")}.png'
#     save_graph(graph_directory, graph_file_name)
#
# if __name__ == '__main__':
#     gen_todays_graph()
#
#
import os
from datetime import date

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utility_functions import get_nba_season_year

matplotlib.use('Agg')


def load_and_concatenate_files(directory):
    """
    Load and concatenate CSV files from a specified directory into a single DataFrame.

    Parameters:
    directory (str): The path to the directory containing CSV files.

    Returns:
    pandas.DataFrame: A DataFrame containing concatenated data from all CSV files in the directory.
                      Returns None if the directory is empty or files are not found.

    Raises:
    FileNotFoundError: If the specified directory does not exist.
    """
    try:
        all_files = os.listdir(directory)
        all_files.sort()  # Ensure files are processed in order
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return None

    dataframes = []
    for filename in all_files:
        try:
            df = pd.read_csv(f'{directory}/{filename}', index_col=None)
            df['Date'] = pd.to_datetime(filename[:8])
            dataframes.append(df)
        except Exception as e:
            print(f"Failed to process file {filename}: {e}")

    return pd.concat(dataframes, axis=0, ignore_index=True) if dataframes else None


def filter_and_resample(frame):
    """
    Filters and resamples a DataFrame to prepare for graph plotting.
    Specifically, it selects players with a 'pred_rank' less than or equal to 5 on the latest date and
    resamples the data weekly.

    Parameters:
    frame (pandas.DataFrame): The DataFrame to be filtered and resampled.

    Returns:
    pandas.DataFrame: The resampled DataFrame.

    Raises:
    ValueError: If the input DataFrame is empty or not formatted correctly.
    """
    if frame is None or frame.empty:
        raise ValueError("Input DataFrame is empty or None")

    players_to_graph = frame.loc[(frame['Date'] == frame.Date.max()) & (frame['pred_rank'] <= 5), 'Player'].tolist()
    filtered_frame = frame[frame['Player'].isin(players_to_graph)]
    return filtered_frame.groupby('Player').resample('W', on='Date').agg('last').drop(columns=['Player']).reset_index().sort_values('pred', ascending=False)
#
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

# def plot_graph(data):
#     """
#     Plots a line graph using seaborn based on the provided DataFrame.
#
#     Parameters:
#     data (pandas.DataFrame): The DataFrame containing the data to plot.
#
#     Returns:
#     None
#
#     Note:
#     This function relies on the current state of matplotlib (plt). Make sure plt is configured correctly before calling.
#     """
#     sns.lineplot(data=data, x='Date', y='pred', hue='Player', marker='o')
#     plt.xticks(rotation=45)
#     plt.yticks([i / 100 for i in range(0, 101, 5)])
#     plt.legend(bbox_to_anchor=(1, 1))
#     plt.tight_layout()
def plot_graph(data, output_directory, graph_file_name):
    """
    Plots and saves a line graph of weekly predicted vote shares for top 5 players.

    Parameters:
    data (pandas.DataFrame): The DataFrame containing the data to plot.
    output_directory (str): The directory path where the graph will be saved.
    graph_file_name (str): The name of the file to save the graph.

    Returns:
    None
    """

    # Ensure 'Date' is a datetime object and 'Week' is correctly formatted
    data['Date'] = pd.to_datetime(data['Date'])
    data['Week'] = data['Date'].dt.to_period('W').dt.start_time

    # Convert 'Predicted Vote Share' from string to float
    data['Predicted Vote Share'] = data['Predicted Vote Share'].str.rstrip('%').astype('float')

    # Identify the most recent week and top 5 players
    most_recent_week = data['Week'].max()
    top_5_players = data[data['Week'] == most_recent_week].nsmallest(5, 'pred_rank')['Player']

    # Filter the DataFrame
    filtered_data = data[data['Player'].isin(top_5_players)]

    # Plotting
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='Week', y='Predicted Vote Share', hue='Player', marker='o')

    # Enhancing the plot
    plt.xticks(rotation=45)
    plt.yticks(range(0, 101, 5))
    plt.gca().set_yticklabels(['{}%'.format(x) for x in range(0, 101, 5)])
    plt.title('Weekly Predicted Vote Shares of Top 5 Players')
    plt.xlabel('Week')
    plt.ylabel('Predicted Vote Share (%)')
    plt.legend(title='Player', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Save the plot
    plt.savefig(f'{output_directory}/{graph_file_name}', dpi=500)




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
    """
    Generates and saves a line graph representing NBA player performance metrics over time.
    """

    sns.set_style('whitegrid')
    frame = load_and_concatenate_files(data_directory)

    if frame is None or frame.empty:
        print('Not enough data points to graph yet.')
        return

    filtered_frame = filter_and_resample(frame)

    # Prepare filename for the line graph
    line_graph_file_name = f'line_graph_{date.today().strftime("%Y%m%d")}.png'
    plot_graph(filtered_frame, output_directory, line_graph_file_name)

    # Prepare filename for the bar graph
    bar_graph_file_name = f'bar_graph_{date.today().strftime("%Y%m%d")}.png'
    # plot_bar_graph(filtered_frame, output_directory, bar_graph_file_name)

    #
    # sns.set_style('whitegrid')
    #
    # try:
    #     directory = f'../ML - Regression/Historic Predictions/{get_nba_season_year()}'
    #     frame = load_and_concatenate_files(directory)
    #
    #     if frame is None or frame.empty:
    #         print('Not enough data points to graph yet.')
    #         return
    #
    #     filtered_frame = filter_and_resample(frame)
    #     plot_graph(filtered_frame)
    #
    #     graph_directory = f'../ML - Regression/Historic Predictions/Graphs/{get_nba_season_year()}'
    #     graph_file_name = f'{date.today().strftime("%Y%m%d")}.png'
    #     save_graph(graph_directory, graph_file_name)
    # except Exception as e:
    #     print(f"An error occurred: {e}")

if __name__ == '__main__':
    data_path = f'../ML - Regression/Historic Predictions/{get_nba_season_year()}'
    output_path = f'../ML - Regression/Historic Predictions/Graphs/{get_nba_season_year()}'

    gen_todays_graph(data_path, output_path)
