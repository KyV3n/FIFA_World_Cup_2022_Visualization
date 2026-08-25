import pandas as pd
from dash import dcc, html
from natsort import natsorted
import plotly.graph_objects as go
import numpy as np

import pandas as pd
df_defense = pd.read_csv('data/defense.csv')
from pages.views_defense.multiple_scatterplot_graph import add_age_bracket, \
    add_age_bracket_equal_division


def defense_plot_distribution_plot_chart():
    return html.Div(
        id="defense_distribution_graph_object",
        children=[
            dcc.Graph(id='defense_violin_plot'),

            html.Br(),

            html.Div([
                dcc.Graph(id='defense_distribution_bar_chart_matches', className='six columns'),
                dcc.Graph(id='defense_distribution_bar_chart_entries', className='six columns')
            ], id='defense_distribution_bar_chart_div')
        ],
    )


def defense_update_violin_plot(y_attribute, n_brackets, equal_division, n_matches):
    """
    Updates the violin plot for distribution section, based on the chosen interactive parameters.
    :param y_attribute: chosen y-axis attribute
    :param n_brackets: chosen number of brackets
    :param equal_division: True of False whether you want the age brackets to be split with an equal amount of
        entries per bracket
    :param n_matches: minimum number of matches played for a played to be taken into account
    :return: updated violin plot figure
    """
    # Drop players with fewer matches than the input 'n_matches'
    df_defense_dropped = df_defense.drop(df_defense[df_defense['minutes_90s'] <= n_matches].index)

    # Drop NaN values if the y-attribute has any
    nan_indices = df_defense_dropped.loc[pd.isna(df_defense_dropped[y_attribute]), :].index
    df_defense_dropped = df_defense_dropped.drop(nan_indices).reset_index(drop=True)

    # Add age brackets to DataFrame, and split depending on whether equal_division is switched on or not
    if not equal_division:
        parts, df_defense_bracket = add_age_bracket(n_brackets, df_defense_dropped)
    else:
        parts, df_defense_bracket = add_age_bracket_equal_division(n_brackets, df_defense_dropped)

    # Round age_float column to 3 decimals
    df_defense_bracket['age_float'] = round(df_defense_bracket['age_float'], 3)

    # Hoverdata
    hoverdata_player_violin = df_defense_bracket['player']
    hoverdata_team_violin = df_defense_bracket['team']
    hoverdata_age_float_violin = df_defense_bracket['age_float']
    hoverdata_matches_violin = df_defense_bracket['minutes_90s']

    # Make violin plot
    fig = go.Figure()
    age_brackets = natsorted(df_defense_bracket["age_bracket"].unique())

    # Fixed colors used for the traces
    # color_list = ['blue', 'orange', 'green', 'pink', 'yellow']
    color_list = ['#77d00c', '#30c769', '#02c199', '#039fc7', '#0f61e8']

    for color_count, age_bracket in enumerate(age_brackets):
        # Hoverdata per sub violin plot
        hoverdata_player_violin_multi = hoverdata_player_violin[df_defense_bracket['age_bracket'] == age_bracket]
        hoverdata_team_violin_multi = hoverdata_team_violin[df_defense_bracket['age_bracket'] == age_bracket]
        hoverdata_age_float_violin_multi = hoverdata_age_float_violin[
            df_defense_bracket['age_bracket'] == age_bracket]
        hoverdata_matches_violin_multi = hoverdata_matches_violin[df_defense_bracket['age_bracket'] == age_bracket]

        fig.add_trace(
            go.Violin(x=df_defense_bracket['age_bracket'][df_defense_bracket['age_bracket'] == age_bracket],
                      y=df_defense_bracket[y_attribute][df_defense_bracket['age_bracket'] == age_bracket],
                      name=age_bracket, box_visible=True, meanline_visible=True, points='all',
                      marker_color=color_list[color_count],
                      customdata=np.stack(
                          (hoverdata_player_violin_multi, hoverdata_team_violin_multi,
                           hoverdata_age_float_violin_multi, hoverdata_matches_violin_multi),
                          axis=-1),
                      hovertemplate=
                      'Value y-attribute: %{y:.3f}<br><br>' +
                      'Player: %{customdata[0]}<br>' +
                      'Team: %{customdata[1]}<br>' +
                      'Age (float): %{customdata[2]: 1f}<br>' +
                      'Playing time (matches): %{customdata[3]}'
                      ))

    return fig


def defense_update_distribution_bar_chart(y_attribute, n_brackets, equal_division, n_matches):
    """
    Updates bar charts for distribution plot section, based on the chosen interactive parameters.
    :param y_attribute: chosen y-axis attribute
    :param n_brackets: chosen number of brackets
    :param equal_division: True of False whether you want the age brackets to be split with an equal amount of
        entries per bracket
    :param n_matches: minimum number of matches played for a played to be taken into account
    :return: updated bar chart figure
    """
    # Drop players with fewer matches than the input 'n_matches'
    df_defense_dropped = df_defense.drop(df_defense[df_defense['minutes_90s'] <= n_matches].index)

    # Drop NaN values if the y-attribute has any
    nan_indices = df_defense_dropped.loc[pd.isna(df_defense_dropped[y_attribute]), :].index
    df_defense_dropped = df_defense_dropped.drop(nan_indices).reset_index(drop=True)

    if n_brackets is not None:
        # Add age brackets to DataFrame, and split depending on whether equal_division is switched on or not
        if equal_division is False:
            parts, df_defense_dropped = add_age_bracket(n_brackets, df_defense_dropped)
        else:
            parts, df_defense_dropped = add_age_bracket_equal_division(n_brackets, df_defense_dropped)

        # Initialize lists
        bracket_sums_list = []

        # For number of brackets
        for i in range(len(parts)):
            # Lower and higher of a single bracket
            lower = parts[i][0]
            higher = parts[i][1]

            # Check whether age_float is in between 'lower' and 'higher'
            in_bracket = df_defense_dropped['age_float'].between(lower, higher)

            # Lists all indices that fall inside the current bracket
            index_list = df_defense_dropped[in_bracket].index

            # Total number of entries/players that are part of the bracket
            sum_entries_bracket = in_bracket.values.sum()

            # Sum of number of matches played by all players that are part of the bracket
            sum_matches_played = df_defense_dropped['minutes_90s'].loc[index_list].sum()

            # Sum of the selected y_attribute by all players that are part of the bracket
            sum_y_attribute = df_defense_dropped[y_attribute].loc[index_list].sum()

            y_per_match = sum_y_attribute / sum_matches_played
            y_per_bracket = sum_y_attribute / sum_entries_bracket

            bracket_sums = {'Bracket': f'{lower}-{higher}',
                            'Number of players': f'{sum_entries_bracket}',
                            f'{y_attribute} / # matches': y_per_match,
                            f'{y_attribute} / # players': y_per_bracket,
                            f'Sum of {y_attribute} over all players': round(sum_y_attribute, 1),
                            f'Number of matches played over all players': round(sum_matches_played, 1)}

            bracket_sums_list.append(bracket_sums)

        df_bracket_averages = pd.DataFrame.from_dict(bracket_sums_list)
        return df_bracket_averages
