import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import os
from tabulate import tabulate

# Do not truncate tables
pd.set_option('display.max_columns', None)

# Load the data
# Match data
df_match_data = pd.read_csv('Data/FIFA World Cup 2022 Match Data/data.csv', delimiter=',')

# Player data
df_player_defense = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_defense.csv', delimiter=',')
df_player_gca = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_gca.csv', delimiter=',')
df_player_keepers = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_keepers.csv', delimiter=',')
df_player_keepersadv = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_keepersadv.csv', delimiter=',')
df_player_misc = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_misc.csv', delimiter=',')
df_player_passing = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_passing.csv', delimiter=',')
df_player_passing_types = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_passing_types.csv', delimiter=',')
df_player_playingtime = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_playingtime.csv', delimiter=',')
df_player_possession = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_possession.csv', delimiter=',')
df_player_shooting = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_shooting.csv', delimiter=',')
df_player_stats = pd.read_csv('Data/FIFA World Cup 2022 Player Data/player_stats.csv', delimiter=',')

# Team data
df_team_data = pd.read_csv('Data/FIFA World Cup 2022 Team Data/team_data.csv', delimiter=',')
df_team_group_stats = pd.read_csv('Data/FIFA World Cup 2022 Team Data/group_stats.csv', delimiter=',')

# Historic data
df_historic_fifa_ranking = pd.read_csv('Data/FIFA World Cup Historic/fifa_ranking_2022-10-06.csv', delimiter=',')
df_historic_matches_1930_2022 = pd.read_csv('Data/FIFA World Cup Historic/matches_1930_2022.csv', delimiter=',')
df_historic_world_cup = pd.read_csv('Data/FIFA World Cup Historic/world_cup.csv', delimiter=',')

# Penalty shootouts
df_penalty_shootouts = pd.read_csv('Data/FIFA World Cup Penalty Shootouts/WorldCupShootouts.csv', delimiter=',')

# Twitter data
df_tweets_01 = pd.read_csv('Data/FIFA World Cup 2022 Twitter Dataset/tweets1.csv', delimiter=';')
df_tweets_02 = pd.read_csv('Data/FIFA World Cup 2022 Twitter Dataset/tweets2.csv', delimiter=';')
df_tweets = pd.concat([df_tweets_01, df_tweets_02])

# Prediction data
df_prediction_groups = pd.read_csv('Data/FIFA World Cup 2022 Prediction/2022_world_cup_groups.csv', delimiter=',')
df_prediction_matches = pd.read_csv('Data/FIFA World Cup 2022 Prediction/2022_world_cup_matches.csv', delimiter=',')
df_prediction_international_matches = pd.read_csv('Data/FIFA World Cup 2022 Prediction/international_matches.csv',
                                                  delimiter=',')
df_prediction_world_cup_matches = pd.read_csv('Data/FIFA World Cup 2022 Prediction/world_cup_matches.csv',
                                              delimiter=',')
df_prediction_world_cups = pd.read_csv('Data/FIFA World Cup 2022 Prediction/world_cups.csv', delimiter=',')