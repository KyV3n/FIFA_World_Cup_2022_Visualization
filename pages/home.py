from dash import html, dcc, register_page, callback, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table
import statsmodels

# Grabbing the dataset for the home page.
df_stats = pd.read_csv('data/player_stats_ratings.csv')
df_stats = df_stats[df_stats['average_rounds'] > 0]
df_stats['age_float'] = df_stats['age_float'].round(2)
df_match_ratings = pd.read_csv('data/ratings.csv')

# Registering the correct page for the multipage support.
register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/'
)

table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

# Find the players with the highest/lowest values automatically
oldest_player = df_stats.loc[df_stats['age_float'].idxmax()]
youngest_player = df_stats.loc[df_stats['age_float'].idxmin()]
lowest_rated_player = df_stats.loc[df_stats['average_rounds'].idxmin()]
highest_rated_player = df_stats.loc[df_stats['average_rounds'].idxmax()]

total_games_row = html.Tr([html.Td("Total games played"), html.Td(len(df_match_ratings))])
average_age_row = html.Tr([html.Td("Average age"), html.Td(df_stats['age_float'].mean().round(2))])
average_rating_row = html.Tr([html.Td("Average rating"), html.Td(df_stats['average_rounds'].mean().round(2))])
oldest_player_row = html.Tr([html.Td("Oldest player"), html.Td(f"{oldest_player['age_float'].round(2)} - {oldest_player['player']}")])
youngest_player_row = html.Tr([html.Td("Youngest player"), html.Td(f"{youngest_player['age_float'].round(2)} - {youngest_player['player']}")])
lowest_rated_player_row = html.Tr([html.Td("Lowest average rating"), html.Td(f"{lowest_rated_player['average_rounds'].round(2)} - {lowest_rated_player['player']}")])
highest_rated_player_row = html.Tr([html.Td("Highest average rating"), html.Td(f"{highest_rated_player['average_rounds'].round(2)} - {highest_rated_player['player']}")])

summary_statistics_body = [html.Tbody([total_games_row, average_age_row, average_rating_row, oldest_player_row,
                                       youngest_player_row, lowest_rated_player_row, highest_rated_player_row])]

# List of tournament rounds
TOURNAMENT_ROUNDS = ['Group Stage', 'Round of 16', 'Quarter-Finals', 'Semi-Finals', '3rd Finals', 'Finals']

# Map tournament rounds to round IDs
ROUND_COLUMNS = {
    'Group Stage': ['Round_1', 'Round_2', 'Round_3'],
    'Round of 16': ['Round_5'],
    'Quarter-Finals': ['Round_27'],
    'Semi-Finals': ['Round_28'],
    '3rd Finals': ['Round_50'],
    'Finals': ['Round_29']
}

def get_teams_for_round(round_name):
    """
    Finds the tournament rounds that the given team has reached.
    :param round_name: stage of the tournament
    :return: all teams that participated in the selected tournament round
    """
    columns = ROUND_COLUMNS.get(round_name)

    if columns is None:
        return []

    teams = []
    for column in columns:
        teams.append(df_stats.loc[df_stats[column] > 0, 'team'])

    return sorted(pd.concat(teams).dropna().unique())

def get_rounds_for_team(team):
    """
    Finds the tournament rounds that the given team has reached.
    :param team: nation name
    :return: all tournament rounds that the given team has reached
    """
    available_rounds = []

    team_df = df_stats[df_stats['team'] == team]

    for round_name, columns in ROUND_COLUMNS.items():
        for column in columns:
            if (team_df[column] > 0).any():
                available_rounds.append(round_name)
                break

    return available_rounds

def filter_player_data(rounds, nation, age_range):
    """
    Filters player data based on tournament round, nation, and age range.

    :param rounds: Selected tournament round.
    :param nation: Selected nation. If None, all nations are included.
    :param age_range: Minimum and maximum age as [min_age, max_age].
    :return: Filtered DataFrame containing players with a rating for the
             selected tournament round.
    """
    # Start with all players
    df_rounds = df_stats.copy()

    # Filter by nation
    if nation:
        df_rounds = df_rounds[df_rounds['team'] == nation]

    # Filter by age
    df_rounds = df_rounds[
        (df_rounds['age_float'] >= age_range[0]) &
        (df_rounds['age_float'] <= age_range[1])
    ]

    # Determine which columns contain the rating for the selected round
    columns = ROUND_COLUMNS.get(rounds)

    if columns is None:
        return df_rounds

    # Group Stage has multiple rounds, so calculate their average
    if rounds == 'Group Stage':
        df_rounds['average_rounds'] = (
            df_rounds[columns].mean(axis=1).round(1)
        )
    else:
        df_rounds['average_rounds'] = df_rounds[columns[0]]

    # Remove players who did not receive a rating in this round
    df_rounds = df_rounds[df_rounds['average_rounds'] > 0]

    return df_rounds

def update_round_nation_filters(rounds, nation, stage_id, nation_id):
    """
    Updates the "round" and "nation" filters based on what "round" or "nation" is currently selected
    :param rounds: all available rounds
    :param nation: selected nation
    :param stage_id: dash stage filter ID
    :param nation_id: dash nation filter ID
    """
    all_rounds = TOURNAMENT_ROUNDS
    all_nations = sorted(df_stats['team'].dropna().unique())

    triggered = ctx.triggered_id

    # User changed ROUND
    if triggered == stage_id:
        available_nations = get_teams_for_round(rounds)

        # Keep nation if it is still valid
        if nation in available_nations:
            selected_nation = nation
        else:
            selected_nation = None

        return (
            [{'label': r, 'value': r} for r in all_rounds], rounds,
            [{'label': t, 'value': t} for t in available_nations], selected_nation
        )

    # User changed NATION
    if triggered == nation_id:
        # No nation selected, so restore all rounds
        if nation is None:

            available_nations = get_teams_for_round(rounds)

            return (
                [{'label': r, 'value': r} for r in all_rounds], rounds,
                [{'label': t, 'value': t} for t in available_nations], None
            )

        # Nation selected, so restrict available rounds (only show rounds reached by that nation)
        available_rounds = get_rounds_for_team(nation)

        # Keep current round if valid
        if rounds in available_rounds:
            selected_round = rounds
        else:
            selected_round = (available_rounds[-1] if available_rounds else None)

        return (
            [{'label': r, 'value': r} for r in available_rounds], selected_round,
            [{'label': t, 'value': t} for t in all_nations], nation
        )

    # Initial load
    available_nations = get_teams_for_round(rounds)

    return (
        [{'label': r, 'value': r} for r in all_rounds], rounds,
        [{'label': t, 'value': t} for t in available_nations], nation
    )

def update_age_filter(slider, min_age, max_age, triggered_id, slider_id):
    """
    Synchronizes the age range slider with the minimum and maximum age inputs.

    :param slider: current [minimum, maximum] values of the age range slider.
    :param min_age: current minimum age entered in the number input.
    :param max_age: current maximum age entered in the number input.
    :param triggered_id: ID of the Dash component that triggered the callback.
    :param slider_id: ID of the age range slider being synchronized.
    """
    if triggered_id == slider_id:
        return slider, slider[0], slider[1]

    if min_age is not None and max_age is not None and min_age <= max_age:
        return [min_age, max_age], min_age, max_age

    return slider, slider[0], slider[1]

def age_selector_dash_component(prefix):
    """
    Reusable Dash component for the age selector.
    :param prefix: Dash component ID prefix.
    """
    return html.Div([
        html.Label("Minimum age"),
        dcc.Input(id=f'{prefix}-age-min', type='number', value=18, min=18, max=40, step=1, debounce=True,
                  style={'width': '170px'}),
        dcc.RangeSlider(id=f'{prefix}-age-slider', min=18, max=40, step=1, value=[18, 40],
                        marks={age: str(age) for age in range(18, 41, 2)}),
        html.Label("Maximum age"),
        dcc.Input(id=f'{prefix}-age-max', type='number', value=40, min=18, max=40, step=1, debounce=True,
                  style={'width': '170px'})
    ])

layout = html.Div([
    # Div for the introduction.
    html.Div(
        children=[
            html.Div(
                children=[
                    html.H5('Does age define football in the 2022 World Cup?'),
                    html.Tr('In this analytical website, we explore the potential relationship between age and football performance.'),
                    html.Tr('Across the different pages, we examine how age relates to different playing positions and how performance may vary throughout a player’s career.'),
                    html.Tr('Using the provided graphs and analytical tools, this website aims to support research into the influence of age on football performance and the development of players across different positions.'),
                    html.Strong('Do not forget you can switch to another view in the top-right corner. The defenders page is somewhat more complete than the home page.')
                    ,
                ],
            ),
        ],
        style={'border': '1px', 'width': '95%', 'margin': '20px'},
    ),

    html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Separator line

    # Div for the summary statistics
    html.Div(
        children=[
            # Header
            html.Div(
                children=[
                    html.H5('Summary Statistics'),
                ],
            ),
            # Summary statistics
            html.Div(
                children=[
                    html.Div([
                        dbc.Table(
                            summary_statistics_body,
                            bordered=True,
                        )
                    ])
                ],
            ),
        ],
        style={'display': 'grid', 'grid-gap': '15px', 'grid-template-columns': '1fr 4fr', 'text-align': 'center', 'border': '1px', 'width': '95%', 'margin': '20px'},  # You can define a CSS class for styling
    ),

    html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Separator line

    # Div for the table.
    html.Div(
        children=[
            # Div to select round of the tournament, nation and the age range.
            html.Div(
                children=[
                    html.H5('Table'),
                    html.Tr('Select stage of the tournament:'),
                    dcc.Dropdown(
                        options=TOURNAMENT_ROUNDS,
                        value='Group Stage',
                        id='crossfilter-yaxis-table-stage'
                    ),
                    html.Tr('Select nation:'),
                    dcc.Dropdown(
                        options=sorted(df_stats['team'].dropna().unique()),
                        value=None,
                        clearable=True,
                        id='crossfilter-yaxis-table-nation'
                    ),
                    html.Tr('Select age group (inclusive):'),
                    age_selector_dash_component('table'),
                ],
            ),
            # Div for the table for searching players.
            html.Div(
                children=[
                    # Data
                    my_table := dash_table.DataTable(
                        columns=[
                            {'name': 'Name', 'id': 'player'},
                            {'name': 'Rating', 'id': 'average_rounds'},
                            {'name': 'Position', 'id': 'position'},
                            {'name': 'Age', 'id': 'age_float'},
                            {'name': 'Minutes', 'id': 'minutes'}
                        ],
                        data=df_stats.to_dict('records'),
                        page_size=10,

                        style_data={
                            'width': '150px', 'overflow': 'hidden', 'textOverflow': 'ellipsis'
                        })
                ],
            ),
        ],
        style={'display': 'grid', 'grid-gap': '15px', 'grid-template-columns': '1fr 4fr', 'text-align': 'center', 'border': '1px', 'width': '95%', 'margin': '20px'},  # You can define a CSS class for styling
    ),

    html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Separator line

    # Div for the scatterplot.
    html.Div(
        children=[
            # Left div of the scatterplot for selecting stage of tournament, nation and age range.
            html.Div(
                children=[
                    html.H5('Scatterplot'),
                    html.Tr('Select stage of the tournament:'),
                    dcc.Dropdown(
                        options=TOURNAMENT_ROUNDS,
                        value='Group Stage',
                        id='crossfilter-yaxis-scatter-stage'
                    ),
                    html.Tr('Select nation:'),
                    dcc.Dropdown(
                        options=sorted(df_stats['team'].dropna().unique()),
                        value=None,
                        clearable=True,
                        id='crossfilter-yaxis-scatter-nation'
                    ),
                    html.Tr('Select age group (inclusive):'),
                    age_selector_dash_component('scatter'),
                ],
            ),
            # Right div with the scatterplot.
            html.Div(
                children=[
                    dcc.Graph(
                        id='crossfilter-indicator-scatter',
                    )
                ],
            ),
        ],
        style={'display': 'grid', 'grid-gap': '15px', 'grid-template-columns': '1fr 4fr', 'text-align': 'center', 'border': '1px', 'width': '95%', 'margin': '20px'},  # You can define a CSS class for styling
    ),

    html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Separator line

    # Div for the scatter matrix
    html.Div(
        children=[
            # Left div with the options for selecting stage of the tournament, nation and age range.
            html.Div(
                children=[
                    html.H5('Scatterplot matrix'),
                    html.Tr('Select stage of the tournament:'),
                    dcc.Dropdown(
                        options=TOURNAMENT_ROUNDS,
                        value='Group Stage',
                        id='crossfilter-yaxis-matrix-stage'
                    ),
                    html.Tr('Select nation:'),
                    dcc.Dropdown(
                        options=sorted(df_stats['team'].dropna().unique()),
                        value=None,
                        clearable=True,
                        id='crossfilter-yaxis-matrix-nation'
                    ),
                    html.Tr('Select age group (inclusive):'),
                    age_selector_dash_component('multiScatter'),
                ],
            ),
            # Right div with the mentioned heatmap.
            html.Div(
                children=[
                    dcc.Graph(
                        id='crossfilter-indicator-heatmap',
                    )
                ],
            ),
        ],
        style={'display': 'grid', 'grid-gap': '15px', 'grid-template-columns': '1fr 4fr', 'text-align': 'center', 'border': '1px', 'width': '95%', 'margin': '20px'},  # You can define a CSS class for styling
    ),
])

# Table: Data update
@callback(
    Output(my_table, 'data'),
    Input('crossfilter-yaxis-table-stage', 'value'),
    Input('crossfilter-yaxis-table-nation', 'value'),
    Input('table-age-slider', 'value')
)
def update_table(rounds, nation, age_range):
    df_rounds = filter_player_data(rounds, nation, age_range)

    return df_rounds.to_dict('records')

# Table: Round-Nation selection interaction
@callback(
    Output('crossfilter-yaxis-table-stage', 'options'),
    Output('crossfilter-yaxis-table-stage', 'value'),
    Output('crossfilter-yaxis-table-nation', 'options'),
    Output('crossfilter-yaxis-table-nation', 'value'),

    Input('crossfilter-yaxis-table-stage', 'value'),
    Input('crossfilter-yaxis-table-nation', 'value')
)
def update_table_round_nation_filters(rounds, nation):
    return update_round_nation_filters(
        rounds, nation, stage_id='crossfilter-yaxis-table-stage', nation_id='crossfilter-yaxis-table-nation'
    )

# Table: Make age slider and integer input work with each other
@callback(
    Output('table-age-slider', 'value'),
    Output('table-age-min', 'value'),
    Output('table-age-max', 'value'),

    Input('table-age-slider', 'value'),
    Input('table-age-min', 'value'),
    Input('table-age-max', 'value'),

    prevent_initial_call=True
)
def update_table_age_filter(slider, min_age, max_age):
    return update_age_filter(slider, min_age, max_age, triggered_id=ctx.triggered_id, slider_id='table-age-slider',)

# Scatterplot: Update data
@callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    Input('crossfilter-yaxis-scatter-stage', 'value'),
    Input('crossfilter-yaxis-scatter-nation', 'value'),
    Input('scatter-age-slider', 'value')
)
def update_scatterplot(rounds, nation, age_range):
    df_rounds = filter_player_data(rounds, nation, age_range)

    # Rename variables for plotting
    df_rounds['Average rating'] = df_rounds['average_rounds']
    df_rounds['Age'] = df_rounds['age_float']

    # Return a scatterplot with a trendline
    return px.scatter(df_rounds, x='Age', y='Average rating', trendline="ols", color='Average rating',
                      hover_data=['player', 'team', 'position', 'minutes'])

# Scatterplot: Round-Nation selection interaction
@callback(
    Output('crossfilter-yaxis-scatter-stage', 'options'),
    Output('crossfilter-yaxis-scatter-stage', 'value'),
    Output('crossfilter-yaxis-scatter-nation', 'options'),
    Output('crossfilter-yaxis-scatter-nation', 'value'),

    Input('crossfilter-yaxis-scatter-stage', 'value'),
    Input('crossfilter-yaxis-scatter-nation', 'value')
)
def update_scatter_round_nation_filters(rounds, nation):
    return update_round_nation_filters(
        rounds, nation, stage_id='crossfilter-yaxis-scatter-stage', nation_id='crossfilter-yaxis-scatter-nation'
    )

# Scatterplot: Make age slider and integer input work with each other
@callback(
    Output('scatter-age-slider', 'value'),
    Output('scatter-age-min', 'value'),
    Output('scatter-age-max', 'value'),

    Input('scatter-age-slider', 'value'),
    Input('scatter-age-min', 'value'),
    Input('scatter-age-max', 'value'),

    prevent_initial_call=True
)
def update_scatter_age_filter(slider, min_age, max_age):
    return update_age_filter(slider, min_age, max_age, triggered_id=ctx.triggered_id, slider_id='scatter-age-slider')



# Scatterplot matrix: Update data
@callback(
    Output('crossfilter-indicator-heatmap', 'figure'),
    Input('crossfilter-yaxis-matrix-stage', 'value'),
    Input('crossfilter-yaxis-matrix-nation', 'value'),
    Input('multiScatter-age-slider', 'value')
)
def update_scatter_matrix(rounds, nation, age_range):
    df_rounds = filter_player_data(rounds, nation, age_range)

    # Rename and keep column for scatter matrix
    df_rounds['rating'] = df_rounds['average_rounds']
    df_rounds = df_rounds[['age_float', 'rating', 'minutes', 'games']]

    # Returning the scatter matrix.
    return px.scatter_matrix(df_rounds)

# Scatterplot matrix: Round-Nation selection interaction
@callback(
    Output('crossfilter-yaxis-matrix-stage', 'options'),
    Output('crossfilter-yaxis-matrix-stage', 'value'),
    Output('crossfilter-yaxis-matrix-nation', 'options'),
    Output('crossfilter-yaxis-matrix-nation', 'value'),

    Input('crossfilter-yaxis-matrix-stage', 'value'),
    Input('crossfilter-yaxis-matrix-nation', 'value')
)
def update_matrix_round_nation_filters(rounds, nation):
    return update_round_nation_filters(
        rounds, nation, stage_id='crossfilter-yaxis-matrix-stage', nation_id='crossfilter-yaxis-matrix-nation'
    )

# Scatterplot matrix: Make age slider and integer input work with each other
@callback(
    Output('multiScatter-age-slider', 'value'),
    Output('multiScatter-age-min', 'value'),
    Output('multiScatter-age-max', 'value'),

    Input('multiScatter-age-slider', 'value'),
    Input('multiScatter-age-min', 'value'),
    Input('multiScatter-age-max', 'value'),

    prevent_initial_call=True
)
def update_multi_age(slider, min_age, max_age):
    return update_age_filter(slider, min_age, max_age, triggered_id=ctx.triggered_id, slider_id='multiScatter-age-slider')