team_mapping = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BKN',
    'Charlotte Bobcats': 'CHA',
    'Charlotte Hornets': 'CHO',  # For the current team, consider context for historical usage
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'Kansas City Kings': 'KCK',
    'Los Angeles Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Jersey Nets': 'NJN',
    'New Orleans Hornets': 'NOH',
    'New Orleans Pelicans': 'NOP',
    'New Orleans/Oklahoma City Hornets': 'NOK',  # Temporary name due to Hurricane Katrina
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHX',
    # 'Phoenix Suns': 'PHO',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'San Diego Clippers': 'SDC',
    'Seattle SuperSonics': 'SEA',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Vancouver Grizzlies': 'VAN',
    'Washington Bullets': 'WSB',
    'Washington Wizards': 'WAS'
}
team_mapping_inverted = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'BKN': 'Brooklyn Nets',
    'BRK': 'Brooklyn Nets',
    'CHH': 'Charlotte Hornets',  # Original Charlotte Hornets before the Bobcats
    'CHA': 'Charlotte Bobcats',  # Historical name
    'CHO': 'Charlotte Hornets',  # Current name
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'KCK': 'Kansas City Kings',  # Historical name
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NJN': 'New Jersey Nets',  # Historical name
    'NOH': 'New Orleans Hornets',  # Historical name
    'NOP': 'New Orleans Pelicans',
    'NOK': 'New Orleans/Oklahoma City Hornets',  # Temporary name due to Hurricane Katrina
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'PHO': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'SDC': 'San Diego Clippers',  # Historical name
    'SEA': 'Seattle SuperSonics',  # Historical name
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'VAN': 'Vancouver Grizzlies',  # Historical name
    'WSB': 'Washington Bullets',  # Historical name
    'WAS': 'Washington Wizards'
}
team_conference_mapping = {
    "Atlanta Hawks": "East",
    "Boston Celtics": "East",
    "Brooklyn Nets": "East",
    "Charlotte Hornets": "East",  # Covers both the original and current Charlotte Hornets
    "Charlotte Bobcats": "East",  # Historical name
    "Chicago Bulls": "East",
    "Cleveland Cavaliers": "East",
    "Dallas Mavericks": "West",
    "Denver Nuggets": "West",
    "Detroit Pistons": "East",
    "Golden State Warriors": "West",
    "Houston Rockets": "West",
    "Indiana Pacers": "East",
    "Kansas City Kings": "West",  # Historical name
    "Los Angeles Clippers": "West",
    "Los Angeles Lakers": "West",
    "Memphis Grizzlies": "West",
    "Miami Heat": "East",
    "Milwaukee Bucks": "East",
    "Minnesota Timberwolves": "West",
    "New Jersey Nets": "East",  # Historical name
    "New Orleans Hornets": "West",  # Historical name
    "New Orleans Pelicans": "West",
    "New Orleans/Oklahoma City Hornets": "West",  # Temporary name due to Hurricane Katrina
    "New York Knicks": "East",
    "Oklahoma City Thunder": "West",
    "Orlando Magic": "East",
    "Philadelphia 76ers": "East",
    "Phoenix Suns": "West",
    "Portland Trail Blazers": "West",
    "Sacramento Kings": "West",
    "San Antonio Spurs": "West",
    "San Diego Clippers": "West",  # Historical name
    "Seattle SuperSonics": "West",  # Historical name
    "Toronto Raptors": "East",
    "Utah Jazz": "West",
    "Vancouver Grizzlies": "West",  # Historical name
    "Washington Bullets": "East",  # Historical name
    "Washington Wizards": "East"
}




if __name__ == '__main__':

    import os
    import pandas as pd

    team_data_dir = '../Basketball Reference Stat Scraper/team_stats/'

    full_data = []
    for year in range(1980, 2023):
        team_data = pd.read_csv(os.path.join(team_data_dir, f'{year}_tm_stats.csv'), index_col=0)

        full_data.append(team_data)
    df = pd.concat(full_data)

    df.Team = df.Team.str.strip('*')
    print(df[~df.Team.str.contains('League')].Team.unique())

    # print(df.Team.unique())