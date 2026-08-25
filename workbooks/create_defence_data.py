from all_data import *
from pathlib import Path

if __name__ == '__main__':
    # Focus only on players whose main position is defender
    df_defense = df_player_defense[['player', 'team']].loc[df_player_defense['position'] == 'DF']
    # Add player club from a different DataFrame
    df_defense = pd.concat([df_defense, df_player_stats[['club']].loc[df_player_stats['position'] == 'DF']], axis=1)

    # Create DataFrame with defenders age
    df_defense_age_full = df_player_defense[['age']].loc[df_player_defense['position'] == 'DF'].copy()
    df_defense_age = df_defense_age_full['age'].str.partition('-', True)
    df_defense['age_years'] = df_defense_age[0]
    df_defense['age_float'] = (df_defense_age[0].astype(int) + (df_defense_age[2].astype(int) / 365)).round(4)

    # Check DataFrame
    print(tabulate(df_defense.head(), headers='keys'))
    print(df_defense.shape)
    print()

    # Add various relevant defender statistics to the DataFrame
    # Defensive
    df_defense = pd.concat([df_defense, df_player_defense[['age', 'minutes_90s', 'tackles', 'tackles_won']].loc[df_player_defense['position'] == 'DF']], axis=1)
    df_defense['succesful_tackles_pct'] = (df_player_defense['tackles_won'] / df_player_defense['tackles']).round(4)
    df_defense = pd.concat([df_defense, df_player_defense[['tackles_def_3rd', 'tackles_mid_3rd', 'dribble_tackles', 'dribbled_past', 'dribbles_vs', 'dribble_tackles_pct', 'blocks', 'blocked_shots', 'blocked_passes', 'interceptions', 'tackles_interceptions', 'clearances', 'errors']].loc[df_player_defense['position'] == 'DF']], axis=1)
    # Possession
    df_defense = pd.concat([df_defense, df_player_possession[['touches', 'touches_def_pen_area']].loc[df_player_possession['position'] == 'DF']], axis=1)
    df_defense['touches_def_pen_area_pct'] = (df_defense['touches_def_pen_area'] / df_defense['touches']).round(4)
    df_defense = pd.concat([df_defense, df_player_possession[['touches_def_3rd', 'touches_mid_3rd', 'miscontrols', 'dispossessed', 'passes_received']].loc[df_player_possession['position'] == 'DF']], axis=1)
    # Passing
    df_defense = pd.concat([df_defense, df_player_passing[['passes_completed', 'passes', 'passes_pct', 'passes_progressive_distance', 'assisted_shots', 'passes_into_final_third', 'progressive_passes']].loc[df_player_passing['position'] == 'DF']], axis=1)
    df_defense = pd.concat([df_defense, df_player_passing_types[['passes_dead', 'through_balls', 'passes_switches', 'passes_blocked']].loc[df_player_passing_types['position'] == 'DF']], axis=1)
    # Miscellaneous
    df_defense = pd.concat([df_defense, df_player_misc[['cards_yellow', 'cards_red', 'fouls', 'fouled', 'pens_conceded', 'own_goals', 'ball_recoveries', 'aerials_won', 'aerials_lost', 'aerials_won_pct']].loc[df_player_misc['position'] == 'DF']], axis=1)
    # Creating actions
    df_defense = pd.concat([df_defense, df_player_gca[['sca_fouled', 'sca_defense', 'gca_fouled', 'gca_defense']].loc[df_player_gca['position'] == 'DF']], axis=1)

    # Check DataFrame
    print(tabulate(df_defense.head(), headers='keys'))
    print(df_defense.shape)
    print()

    # # Remove players with very little playing time (less than half a match)
    # df_defense = df_defense.drop(df_defense[df_defense['minutes_90s'] <= 0.5].index)

    # Check DataFrame
    print(tabulate(df_defense.head(), headers='keys'))
    print(df_defense.shape)
    print()

    # Every row with at least one NaN value
    print(tabulate(df_defense[df_defense.isnull().any(axis=1)], headers='keys'))
    print()

    # Data exploration: Unique players and ages
    print(sorted(df_defense['age_years'].unique()))
    unique_player = len(df_defense['player'].unique())
    print(f'Number of unique players: {unique_player}')
    unique_age = len(df_defense['age_years'].unique())
    print(f'Number of unique ages: {unique_age}')

    # Data exploration: select players from specific teams
    df_selected_team = df_defense[df_defense.team.isin(['Qatar', 'Senegal'])]
    print(tabulate(df_selected_team.head(), headers='keys'))

    # Data exploration: select specific players by name
    df_selected_team = df_defense[df_defense.player.isin(['Abdou Diallo', 'Abdulelah Al-Amri'])]
    print(tabulate(df_selected_team.head(), headers='keys'))

    # # Heatmap all variables correlation
    # df_test = df_defense.copy()
    # df_test.drop(['player', 'team', 'club', 'age'], axis=1, inplace=True)
    # print(tabulate(df_test.head(), headers='keys'))
    #
    # fig, ax = plt.subplots(figsize=(40, 35))
    # sns.heatmap(df_test.corr(), ax=ax, annot=True)
    # # plt.savefig('Player Defense Correlation Heatmap')
    # plt.show()

    # Export final defenders CSV
    output_path = Path(__file__).resolve().parent.parent / "data" / "defense.csv"
    df_defense = df_defense.reset_index(drop=True)
    df_defense.to_csv(path_or_buf=output_path)