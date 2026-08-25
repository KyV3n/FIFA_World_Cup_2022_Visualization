# Import libraries
from curl_cffi import requests
import pandas as pd
import csv
from pathlib import Path

# Request headers
headers = {'X-Requested-With': 'XMLHttpRequest'}

# Lists used to store results
list_of_matches = []
ratings_matches = []
ratings = []

# Local data files
csv_file_match_data = "Data/FIFA World Cup 2022 Match Data/data.csv"
df_match_data = pd.read_csv(csv_file_match_data)

# Scrape the World Cup group-stage matches from SofaScore
def scrapeGroupStage():
    for id in range(3954, 3962):
        url = (f'https://api.sofascore.com/api/v1/tournament/{id}/season/41087/events')
        r = requests.get(url, headers=headers, impersonate='chrome', timeout=20)

        print(f'Group stage request status: {r.status_code}')
        r.raise_for_status()

        data = r.json()

        for x in data['events']:
            list_of_matches.append([x['id'], x['roundInfo']['round'], x['homeTeam']['name'], x['awayTeam']['name']])

# Scrape the World Cup knockout-stage matches from SofaScore
def scrapeKnockoutStage():
    url = ('https://api.sofascore.com/api/v1/unique-tournament/16/season/41087/events/last/0')
    r = requests.get(url, headers=headers, impersonate='chrome', timeout=20)

    print(f'Knockout stage request status: {r.status_code}')
    r.raise_for_status()

    data = r.json()

    for x in data['events']:
        if x['tournament']['slug'] == "world-cup-knockout-stage":
            list_of_matches.append([x['id'], x['roundInfo']['round'], x['homeTeam']['name'], x['awayTeam']['name']])

# Scrape the lineups and player ratings for a specific match
def scrapeRatings(matchID, matchRound, homeTeam, awayTeam):
    url = (f'https://api.sofascore.com/api/v1/event/{matchID}/lineups')

    r = requests.get(url, headers=headers, impersonate='chrome', timeout=20)

    print(f'Scraping match: {homeTeam} vs {awayTeam}. Status: {r.status_code}')
    r.raise_for_status()

    data = r.json()

    # Add match information to the lineup response
    data['event'] = matchID
    data['round'] = matchRound
    data['homeTeam'] = homeTeam
    data['awayTeam'] = awayTeam

    ratings_matches.append(data)

# Scrape all group-stage and knockout-stage matches
scrapeGroupStage()
scrapeKnockoutStage()
print(list_of_matches)
print(f'Total matches found: {len(list_of_matches)}\n')

# Scrape the player ratings for every match
for x in list_of_matches:
    scrapeRatings(x[0], x[1], x[2], x[3])
print(f'Rating datasets collected: {len(ratings_matches)}\n')

# Process the player ratings for each match
for match in ratings_matches:
    match_dict = {}
    ratings_home = []
    ratings_away = []

    # Process home-team players
    for player in match['home']['players']:
        dict_rating = {}

        # Add player name
        dict_rating['player_name'] = player['player']['name']

        # Standardize country names to match the existing dataset
        if player['player']['country']['name'] == 'Iran':
            dict_rating['player_country'] = 'IR Iran'
        elif player['player']['country']['name'] == 'USA':
            dict_rating['player_country'] = 'United States'
        elif player['player']['country']['name'] == 'South Korea':
            dict_rating['player_country'] = 'Korea Republic'
        else:
            dict_rating['player_country'] = player['player']['country']['name']

        # Some players may not have a rating
        try:
            dict_rating['player_rating'] = player['statistics']['rating']
        except KeyError:
            dict_rating['player_rating'] = None

        ratings_home.append(dict_rating)

    # Process away-team players
    for player in match['away']['players']:
        dict_rating = {}

        # Add player name
        dict_rating['player_name'] = player['player']['name']

        # Standardize country names to match the existing dataset
        if player['player']['country']['name'] == 'Iran':
            dict_rating['player_country'] = 'IR Iran'
        elif player['player']['country']['name'] == 'USA':
            dict_rating['player_country'] = 'United States'
        elif player['player']['country']['name'] == 'South Korea':
            dict_rating['player_country'] = 'Korea Republic'
        else:
            dict_rating['player_country'] = player['player']['country']['name']

        # Some players may not have a rating
        try:
            dict_rating['player_rating'] = player['statistics']['rating']
        except KeyError:
            dict_rating['player_rating'] = None

        ratings_away.append(dict_rating)

    # Standardize team names to match the existing dataset
    if match['homeTeam'] == 'Iran':
        match['homeTeam'] = 'IR Iran'
    elif match['homeTeam'] == 'USA':
        match['homeTeam'] = 'United States'
    elif match['homeTeam'] == 'South Korea':
        match['homeTeam'] = 'Korea Republic'

    if match['awayTeam'] == 'Iran':
        match['awayTeam'] = 'IR Iran'
    elif match['awayTeam'] == 'USA':
        match['awayTeam'] = 'United States'
    elif match['awayTeam'] == 'South Korea':
        match['awayTeam'] = 'Korea Republic'

    # Match the SofaScore fixture to the corresponding match in the CSV
    print(f"Home team: {match['homeTeam']} vs Away Team: {match['awayTeam']}")
    query = df_match_data.loc[
        (df_match_data['home_team'] == match['homeTeam']) &
        (df_match_data['away_team'] == match['awayTeam'])
    ]
    print(f'Local match ID: {query['match'].item()}')

    # Build the final dictionary for this match
    match_dict['match'] = query['match'].item()
    match_dict['round'] = match['round']
    match_dict['home_team'] = match['homeTeam']
    match_dict['away_team'] = match['awayTeam']
    match_dict['home_ratings'] = ratings_home
    match_dict['away_ratings'] = ratings_away

    ratings.append(match_dict)
print()

# Write all match ratings to a CSV file
csv_columns = ['match', 'round', 'home_team', 'away_team', 'home_ratings', 'away_ratings']
output_path = Path(__file__).resolve().parent.parent / "data" / "ratings.csv"

try:
    with open(output_path, 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in ratings:
            writer.writerow(data)
except IOError:
    print("I/O error")

# Show ratings DataFrame
df_ratings = pd.read_csv(output_path, converters={'home_ratings': eval, 'away_ratings': eval})
print(df_ratings)

# Player stats DataFrame
player_stats = 'Data/FIFA World Cup 2022 Player Data/player_stats.csv'
df_stats = pd.read_csv(player_stats)

# Add each player's SofaScore rating to the corresponding match column
for idx in df_ratings.index:
    # Get the match/round number and the player ratings for both teams
    wc_round = df_ratings['round'][idx]
    list_home_ratings = (df_ratings['home_ratings'][idx])
    list_away_ratings = (df_ratings['away_ratings'][idx])

    # Match players in the rating and player stats DataFrames
    for player in list_home_ratings:
        df_stats.loc[df_stats['player'] == player['player_name'], f'Round_{wc_round}'] = player['player_rating']
    for player in list_away_ratings:
        df_stats.loc[df_stats['player'] == player['player_name'], f'Round_{wc_round}'] = player['player_rating']

# All the match/round columns
# Rounds 1, 2, 3: Group stage. Round 5: Round of 16. Round 27: Quarterfinals. Round 28: Semifinals.
# Round 50: 3rd place final. Round 29: Final
round_columns = ['Round_1', 'Round_2', 'Round_3', 'Round_5', 'Round_27', 'Round_28', 'Round_50', 'Round_29']

# Calculate each player's average rating across the matches they played in
df_stats['average_rounds'] = df_stats[round_columns].mean(axis=1).round(2)
print(df_stats)

# Add separated age
age = df_stats['age'].str.partition('-')
df_stats['years'] = age[0].astype(int)
df_stats['days'] = age[2].astype(int)
df_stats['age_float'] = df_stats['years'] + df_stats['days'] / 365

# Save the updated player statistics to a new CSV file
output_path = Path(__file__).resolve().parent.parent / "data" / "player_stats_ratings.csv"
df_stats.to_csv(path_or_buf=output_path)