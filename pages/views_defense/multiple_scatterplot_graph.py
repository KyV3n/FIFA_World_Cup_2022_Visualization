import numpy as np
import plotly.graph_objs as go
from dash import dcc, html
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

import pandas as pd
df_defense = pd.read_csv('data/defense.csv')


def defense_plot_multi_scatterplot_chart():
    return html.Div(
        id="defense_multi_scatterplot_graph_object",
        children=[
            dcc.Graph(id='defense_multi_scatterplot')
        ],
    )


def add_age_bracket(n_brackets, df_defense_dropped):
    """
    Adds a column with the age bracket a player belongs to. The age brackets will be split according to an equal split
        on the age ranges. So every bracket covers the same number of ages.
    :param n_brackets: chosen number of brackets to be split
    :param df_defense_dropped: df_defense after entries with NaN values are dropped
    :return: df_defense_dropped, with an added 'age_bracket' column + list of lists of brackets
    """

    def round_integer(x):
        i, f = divmod(x, 1)
        return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

    if n_brackets is not None:
        # Change lowest/highest age dynamically with the minimum number of matches played (different brackets)
        # highest_age = int(df_defense['age_years'].max()) + 1
        # lowest_age = int(df_defense['age_years'].min())

        # Stationary lowest/highest age dynamically with the minimum number of matches played (brackets do not change)
        highest_age = 40
        lowest_age = 19

        # Initialization for bracket splitting
        part_length = (highest_age - lowest_age) / n_brackets
        parts = []
        marker = lowest_age

        # Splits into brackets, in the form of a list of lists
        for _ in range(n_brackets):
            part = [round_integer(marker), round_integer(marker + part_length)]
            marker += part_length
            parts.append(part)

        # Adds the 'age_bracket' column to the dataframe, according to the gotten brackets
        df_defense_dropped['age_bracket'] = ''
        for i in range(len(parts)):
            lower = parts[i][0]
            higher = parts[i][1]

            in_bracket = df_defense_dropped['age_float'].between(lower, higher)
            index_list = df_defense_dropped[in_bracket].index

            df_defense_dropped.loc[index_list, 'age_bracket'] = f'{lower}-{higher}'

        return parts, df_defense_dropped


def add_age_bracket_equal_division(n_brackets, df_defense_dropped):
    """
    Adds a column with the age bracket a player belongs to. The age brackets will be split according to the amount of
        items in each bracket.
    :param n_brackets: chosen amount of brackets to be split
    :param df_defense_dropped: df_defense after entries with NaN values are dropped
    :return: df_defense_dropped, with an added 'age_bracket' column + list of lists of brackets
    """
    if n_brackets is not None:
        # Sorts dataframe from lowest to highest on 'age_float'
        df_defense_sorted = df_defense_dropped.sort_values('age_float').reset_index(drop=True).copy()
        df_defense_sorted['age_bracket'] = ''

        # Split row positions into approximately equal-sized groups
        indices = np.array_split(np.arange(len(df_defense_sorted)), n_brackets)

        chunks = [
            df_defense_sorted.iloc[indexes].copy()
            for indexes in indices
            if len(indexes) > 0
        ]

        # Initialize new dataframe and age bracket list
        df_merged = pd.DataFrame()
        parts = []

        # print(tabulate(chunks[0], headers='keys'))
        # print(tabulate(chunks[1], headers='keys'))
        # print(round(chunks[0]['age_float'].iloc[-1], 3))
        for i, chunk in enumerate(chunks):
            if i != len(chunks) - 1:
                middle = (chunks[i]['age_float'].iloc[-1] + chunks[i + 1]['age_float'].iloc[0]) / 2
                higher_bound = round(middle, 2)

            if i == 0:
                lower_bound = round(chunk['age_float'].iloc[0] - 0.05, 2)
            if i == len(chunks) - 1:
                higher_bound = round(chunk['age_float'].iloc[-1] + 0.05, 2)

            # Adds lowest and highest value for 'age_float' and rounds to nearest integer to add as new column
            # 'age_bracket'
            chunk['age_bracket'] = f'{lower_bound}-{higher_bound}'

            # Put age brackets into list
            part = [lower_bound, higher_bound]
            parts.append(part)

            df_merged = pd.concat([df_merged, chunk])

            lower_bound = higher_bound

        # print(parts)
        return parts, df_merged

def extract_data(df, y_attribute):
    """
    Extracts data for the x and y-axis and removes all entries with NaN value
    :param df: any given dataframe
    :param y_attribute: chosen y-attribute
    :return: Series object data for x and y-axis, and a DataFrame with NaN values dropped
    """
    # Extract data
    x = df['age_float']
    y = df[y_attribute]

    # Remove entries with NaN value
    nan_indices = df.loc[pd.isna(df[y_attribute]), :].index
    x = x.drop(nan_indices).reset_index(drop=True)
    y = y.drop(nan_indices).reset_index(drop=True)

    df_defense_dropped = df.drop(nan_indices).reset_index(drop=True)

    return x, y, df_defense_dropped


def fit_quadratic_curve(x, y):
    """
    Fits a quadratic curve line using SkLearn, which will be plotted as a trace in a scatterplot
    :param x: data for x-axis
    :param y: data for y-axis
    :return: quadratic fit line
    """
    # Fit quadratic curve
    model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    model.fit(np.array(x).reshape(-1, 1), y)
    x_reg = np.linspace(x.min(), x.max(), 100)
    y_reg = model.predict(x_reg.reshape(-1, 1))

    return x_reg, y_reg


def plot_scatterplot_traces_multi(x, y, multi_selection, all_data, y_attribute, df_defense_matches):
    """
    Plots a scatterplot with multiple fit lines and point traces. First extract the data for the selected data,
    then fits the quadratic curve, then adds the traces, then update plot layout and finally plot the scatterplot.
    :param x: data for x-axis
    :param y: data for y-axis
    :param multi_selection: selected items to make separate fit lines off
    :param all_data: all data for the selected item
    :param y_attribute: chosen y-attribute
    :return: scatterplot with traces for data points and fit lines
    """
    # Custom hoverdata for player and team
    hoverdata_player = df_defense_matches['player']
    hoverdata_team = df_defense_matches['team']
    hoverdata_matches = df_defense_matches['minutes_90s']

    # Remove entries with NaN value
    nan_indices = df_defense_matches.loc[pd.isna(df_defense_matches[y_attribute]), :].index

    # Drop NaN values for custom hoverdata for player and team
    hoverdata_player_dropped = hoverdata_player.drop(nan_indices).reset_index(drop=True)
    hoverdata_team_dropped = hoverdata_team.drop(nan_indices).reset_index(drop=True)
    hoverdata_matches_dropped = hoverdata_matches.drop(nan_indices).reset_index(drop=True)

    # Plot
    fig = go.Figure()

    # Fixed colors used for the traces
    # color_list = ['blue', 'orange', 'green', 'pink', 'yellow']
    color_list = ['#77d00c', '#30c769', '#02c199', '#039fc7', '#0f61e8']

    color_count = 0

    # Fit quadratic curve for every selected team
    for item in multi_selection:
        x_multi = x[all_data == item]
        y_multi = y[all_data == item]
        hoverdata_player_multi = hoverdata_player_dropped[all_data == item]
        hoverdata_team_multi = hoverdata_team_dropped[all_data == item]
        hoverdata_matches_multi = hoverdata_matches_dropped[all_data == item]

        x_reg, y_reg = fit_quadratic_curve(x_multi, y_multi)

        # Add scatterplot points
        fig.add_trace(
            go.Scatter(x=x_multi, y=y_multi, mode='markers', name=f'{item} Observations', opacity=0.5,
                       marker_color=color_list[color_count],
                       customdata=np.stack((hoverdata_player_multi, hoverdata_team_multi,
                                            hoverdata_matches_multi), axis=-1),
                       # text=x_multi,
                       hovertemplate=
                       # '<b>%{text}</b><br><br>' +
                       'Value y-attribute: %{y:.3f}<br>' +
                       'Age (float): %{x:.3f}<br><br>' +
                       'Player: %{customdata[0]}<br>' +
                       'Team: %{customdata[1]}<br>' +
                       'Playing time (matches): %{customdata[2]}'
                       ))

        # Add quadratic fit line
        fig.add_trace(go.Scatter(x=x_reg, y=y_reg, mode='lines', name=f'{item} Quadratic Fit Line',
                                 marker_color=color_list[color_count]))

        color_count += 1

    # Update layout
    fig.update_layout(title=f'Scatterplot: {y_attribute.title()} vs age_float',
                      xaxis_title='age_float',
                      yaxis_title=y_attribute.title())
    return fig


def defense_update_multi_scatterplot(y_attribute, n_brackets, selected_teams, equal_division, df_defense_matches):
    """
    Updates the scatterplot traces, based on the selected y_attribute, number of brackets and team
    :param y_attribute: selected attribute for y-axis
    :param n_brackets: selected number of age brackets
    :param selected_teams: selected teams
    :param equal_division: True of False whether you want the age brackets to be split with an equal number of
        entries per bracket
    :param df_defense_matches: df_defense, but with players that have fewer matches played than the selected number
        removed
    :return: updated scatterplot figure
    """
    if n_brackets is None and selected_teams == []:
        # Extract data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)

        # Fit quadratic curves
        x_reg, y_reg = fit_quadratic_curve(x, y)

        # Custom hoverdata for player and team
        hoverdata_player = df_defense['player']
        hoverdata_team = df_defense['team']

        # Remove entries with NaN value
        nan_indices = df_defense.loc[pd.isna(df_defense[y_attribute]), :].index

        # Drop NaN values for custom hoverdata for player and team
        hoverdata_player_dropped = hoverdata_player.drop(nan_indices).reset_index(drop=True)
        hoverdata_team_dropped = hoverdata_team.drop(nan_indices).reset_index(drop=True)

        # Create scatter plot
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Observations', opacity=0.5,
                                 customdata=np.stack((hoverdata_player_dropped, hoverdata_team_dropped), axis=-1),
                                 hovertemplate=
                                 'Value y-attribute: %{y:.3f}<br>' +
                                 'Age (float): %{x:.3f}<br><br>' +
                                 'Player: %{customdata[0]}<br>' +
                                 'Team: %{customdata[1]}'))

        # Add quadratic fit line
        fig.add_trace(go.Scatter(x=x_reg, y=y_reg, mode='lines', name='Quadratic Fit Line'))

        # Update layout
        fig.update_layout(title=f'Scatterplot: {y_attribute.title()} vs age_float',
                          xaxis_title='age_float',
                          yaxis_title=y_attribute.title())
        return fig
    elif n_brackets is not None:
        # Extract data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)

        # Add age brackets to df_defense DataFrame, and split depending on whether equal_division is switched on or not
        if equal_division is False:
            parts, df_defense_bracket = add_age_bracket(n_brackets, df_defense_dropped)
        else:
            parts, df_defense_bracket = add_age_bracket_equal_division(n_brackets, df_defense_dropped)
        age_bracket = df_defense_bracket['age_bracket']

        # Selected brackets
        multi_selection_bracket = sorted(df_defense_bracket['age_bracket'].unique())

        # Plot scatterplot graph with traces
        return plot_scatterplot_traces_multi(x, y, multi_selection_bracket, age_bracket, y_attribute,
                                             df_defense_matches)
    elif selected_teams:
        # Extract data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)
        teams = df_defense_dropped['team']

        # Plot scatterplot graph with traces
        return plot_scatterplot_traces_multi(x, y, selected_teams, teams, y_attribute, df_defense_matches)


def defense_count_multi_scatterplot(y_attribute, n_brackets, selected_teams, equal_division, df_defense_matches):
    """
    Counts number of data points used for every (sub-)scatterplot
    :param y_attribute: selected attribute for y-axis
    :param n_brackets: selected number of age brackets
    :param selected_teams: selected teams
    :param equal_division: True of False whether you want the age brackets to be split with an equal number of entries
        per bracket
    :param df_defense_matches: df_defense, but with players that have fewer matches played than the selected amount
        removed
    :return: number of data points used for every (sub-)selection of data
    """
    if n_brackets is None and selected_teams == []:
        # Extract Data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)
        return f'Number of data points: {y.count()}'
    elif n_brackets is not None:
        # Extract Data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)

        # Add age brackets to df_defense DataFrame, and split depending on whether equal_division is switched on or not
        if equal_division is False:
            parts, df_defense_bracket = add_age_bracket(n_brackets, df_defense_dropped)
        else:
            parts, df_defense_bracket = add_age_bracket_equal_division(n_brackets, df_defense_dropped)
        age_bracket = df_defense_bracket['age_bracket']

        output_text_list = []
        # Find number of data points for every age bracket
        for bracket in sorted(df_defense_bracket['age_bracket'].unique()):
            y_bracket = y[age_bracket == bracket]
            output_text_list.append(f'Number of data points for {bracket}: {y_bracket.count()}')
            output_text_list.append(html.Br())
        return output_text_list
    elif selected_teams:
        # Extract Data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)
        teams = df_defense_dropped['team']

        output_text_list = []
        # Find number of data points for every team
        for selected_team in selected_teams:
            y_team = y[teams == selected_team]
            output_text_list.append(f'Number of data points for {selected_team}: {y_team.count()}')
            output_text_list.append(html.Br())
        return output_text_list


def defense_correlation_multi_scatterplot(y_attribute, n_brackets, selected_teams, equal_division, df_defense_matches):
    """
    Calculates correlation between x and y-axis for every (sub-)scatterplot
    :param y_attribute: selected attribute for y-axis
    :param n_brackets: selected number of age brackets
    :param selected_teams: selected teams
    :param equal_division: True of False whether you want the age brackets to be split with an equal number of entries
        per bracket
    :param df_defense_matches: df_defense, but with players that have fewer matches played than the selected amount
        removed
    :return: correlation for every (sub-)selection of data
    """
    if n_brackets is None and selected_teams == []:
        # Extract Data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)

        return f'Correlation between x and y attribute for: {round(x.corr(y), 3)}'
    elif n_brackets is not None:
        # Extract Data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)

        # Add age brackets to df_defense DataFrame, and split depending on whether equal_division is switched on or not
        if not equal_division:
            parts, df_defense_bracket = add_age_bracket(n_brackets, df_defense_dropped)
        else:
            parts, df_defense_bracket = add_age_bracket_equal_division(n_brackets, df_defense_dropped)
        age_bracket = df_defense_bracket['age_bracket']

        output_text_list = []
        # Find correlation between x and y attribute for every age bracket
        for bracket in sorted(df_defense_bracket['age_bracket'].unique()):
            x_bracket = x[age_bracket == bracket]
            y_bracket = y[age_bracket == bracket]
            output_text_list.append(
                f'Correlation of x and y attribute for {bracket}: {round(x_bracket.corr(y_bracket), 3)}')
            output_text_list.append(html.Br())
        return output_text_list
    elif selected_teams:
        # Extract Data
        x, y, df_defense_dropped = extract_data(df_defense_matches, y_attribute)
        teams = df_defense_dropped['team']

        output_text_list = []
        # Find correlation between x and y attribute for every team
        for selected_team in selected_teams:
            x_team = x[teams == selected_team]
            y_team = y[teams == selected_team]
            output_text_list.append(
                f'Correlation of x and y attribute for {selected_team}: {round(x_team.corr(y_team), 3)}')
            output_text_list.append(html.Br())
        return output_text_list
