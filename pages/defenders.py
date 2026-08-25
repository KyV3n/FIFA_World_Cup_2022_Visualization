from pages.views_defense.config import table_attribute_list

from pages.views_defense.player_search_menu import defense_make_menu_layout_player_search

from pages.views_defense.piechart_menu import defense_make_menu_layout_pie_chart
from pages.views_defense.piechart_graph import (defense_extract_age_bracket_pie_chart,
                                                                       defense_plot_pie_bar_chart)

from pages.views_defense.distribution_plots_menu import \
    defense_make_menu_layout_distribution_plot
from pages.views_defense.distribution_plots_graph import (defense_update_distribution_bar_chart,
                                                                                 defense_update_violin_plot,
                                                                                 defense_plot_distribution_plot_chart)

from pages.views_defense.multiple_scatterplot_menu import \
    defense_make_menu_layout_multi_scatterplot
from pages.views_defense.multiple_scatterplot_graph import (defense_update_multi_scatterplot,
                                                                                   defense_count_multi_scatterplot,
                                                                                   defense_correlation_multi_scatterplot,
                                                                                   defense_plot_multi_scatterplot_chart)

import dash
from dash import dcc, html, dash_table
from dash import register_page, callback  # , callback # If you need callbacks, import it here.

import plotly.express as px

import pandas as pd

df_defense = pd.read_csv('data/defense.csv')
df_defense_dictionary = pd.read_csv('data/defense_dictionary.csv', sep=';')

register_page(
    __name__,
    name='Defenders',
    top_nav=True,
    path='/defenders'
)


def layout():
    layout = (html.Div([

        # Block for player data table search
        html.Div([
            # Left column - Interactions
            html.Div(
                children=defense_make_menu_layout_player_search(),
                id='defense_player_search_interaction',
                className="three columns"),

            # Right column - Table
            html.Div([
                dash_table.DataTable(data=df_defense.to_dict('records'),
                                     columns=[{"name": i, "id": i} for i in df_defense.columns],
                                     style_table={'overflowY': 'scroll', 'maxHeight': '500px'})
            ],
                id='defense_player_search_table_output',
                className="nine columns"),
        ], id="app_container_player_search", style={'width': '100%', 'display': 'inline-block'}),

        html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Seperator line

        # Block for part-to-whole (Pie Chart + Bar Chart)
        html.Div([
            # Left column - Dropdown menu interactions
            html.Div(
                children=defense_make_menu_layout_pie_chart(),
                id="defense_pie-chart_interaction",
                className="three columns"
            ),

            # Right column - Plots
            html.Div(
                children=defense_plot_pie_bar_chart(),
                id="defense_pie-chart_plots_output",
                className="nine columns"),
        ], id="app_container_scatterplot", style={'width': '100%', 'display': 'inline-block'}),

        html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Seperator line

        # Block for distribution charts (violin plot)
        html.Div([
            # Left column - Dropdown menu interactions
            html.Div(
                children=defense_make_menu_layout_distribution_plot(),
                id="defense_distribution_plot_interaction",
                className="three columns"
            ),

            # Right column - Plot
            html.Div(
                children=defense_plot_distribution_plot_chart(),
                id="defense_distribution_plot_output",
                className="nine columns"),
        ], id="app_container_distribution_plot", style={'width': '100%', 'display': 'inline-block'}),

        html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Seperator line

        # Block for multi scatterplot
        html.Div([
            # Left column - Dropdown menu interactions
            html.Div(
                children=defense_make_menu_layout_multi_scatterplot(),
                id="defense_multi_scatterplot_interaction",
                className="three columns"
            ),

            # Right column - Plot
            html.Div(
                children=defense_plot_multi_scatterplot_chart(),
                id="defense_multi_scatterplot_output",
                className="nine columns"),
        ], id="app_container_multi_scatterplot", style={'width': '100%', 'display': 'inline-block'}),

        html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Seperator line

        # Section for dictionary
        html.Div([
            html.H5("Dictionary for attributes"),
            dash_table.DataTable(data=df_defense_dictionary.to_dict('records'),
                                 columns=[{"name": i, "id": i} for i in df_defense_dictionary.columns],
                                 style_table={'overflowY': 'scroll'})
        ],
            id='defense_dictionary'),

        html.Hr(style={'borderWidth': '0.8vh', 'borderColor': '#000000'}),  # Seperator line
    ]))
    return layout


# 1. Section for player search
# Callback 1 - Input menu based on selected attribute to filter on
@callback(
    dash.dependencies.Output('defense_player_search_attribute_input_div', 'children'), [
        dash.dependencies.Input("defense_player_search_select_attribute", "value")
    ])
def defense_player_attribute_input(attribute):
    try:
        return html.Div([
            html.Br(),
            html.B(f"Minimum number of {attribute}:"),
            html.Br(),
            dcc.Input(
                id='defense_player_search_attribute_input',
                type='number', min=0, max=df_defense[attribute].max(),
                placeholder=f"Range: 0-{df_defense[attribute].max()}",
                debounce=True)
        ])
    except KeyError:
        return None


# Callback 2 - Update possible team selections based on selected minimum time played
@callback(
    dash.dependencies.Output("defense_player_search_select_team", 'options'), [
        dash.dependencies.Input("defense_player_search_select_attribute", "value"),
        dash.dependencies.Input('defense_player_search_attribute_input', "value")
    ])
def defense_player_search_team_dropdown(attribute, attribute_value):
    try:
        df_defense_team_selection = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
    except KeyError:
        df_defense_team_selection = df_defense
    team_list = sorted(df_defense_team_selection['team'].unique())
    return [{'label': team, 'value': team} for team in team_list]


# Callback 3 - Update possible player selections based on selected team and minimum time played
@callback(
    dash.dependencies.Output("defense_player_search_select_player", 'options'), [
        dash.dependencies.Input("defense_player_search_select_team", 'value'),
        dash.dependencies.Input("defense_player_search_select_attribute", "value"),
        dash.dependencies.Input('defense_player_search_attribute_input', "value")
    ])
def defense_player_search_player_dropdown(selected_team, attribute, attribute_value):
    if not selected_team:
        try:
            df_defense_player_selection = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
        except KeyError:
            df_defense_player_selection = df_defense
        player_list = df_defense_player_selection['player'].unique()
        return [{'label': player, 'value': player} for player in player_list]
    else:
        try:
            df_defense_player_selection = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
        except KeyError:
            df_defense_player_selection = df_defense
        df_selected_team = df_defense_player_selection[df_defense_player_selection.team.isin(selected_team)]
        player_list = df_selected_team['player'].unique()
        return [{'label': player, 'value': player} for player in player_list]


# Callback 4 - Display the table with the selected players
@callback(
    dash.dependencies.Output('defense_player_search_table_output', "children"), [
        dash.dependencies.Input("defense_player_search_select_attribute", "value"),
        dash.dependencies.Input('defense_player_search_attribute_input', "value"),
        dash.dependencies.Input("defense_player_search_select_team", 'value'),
        dash.dependencies.Input("defense_player_search_select_player", 'value'),
    ], prevent_initial_call=True)
def defense_player_search_dash_table(attribute, attribute_value, selected_team, selected_player):
    def defense_update_table(attribute, attribute_value, selected_team, selected_player, df_defense):
        def defense_player_data(df_defense_short):
            return dash_table.DataTable(
                data=df_defense_short.to_dict('records'),
                columns=[{"name": i, "id": i} for i in table_attribute_list],
                style_table={'overflowY': 'scroll', 'maxHeight': '500px'}
            )

        if selected_team == [] and selected_player == []:  # If no team and player is selected
            # Display data for all players that played at least the number of the selected minutes_90s
            df_defense_short = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
            return defense_player_data(df_defense_short)
        elif selected_team != [] and selected_player == []:  # If at least one team, but no player is selected
            try:
                # Display data for players from the selected team(s) and a playing time of at least the selected minutes_90s
                df_defense_short = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
            except KeyError:
                df_defense_short = df_defense
            df_defense_short = df_defense_short[df_defense_short.team.isin(selected_team)]
            return defense_player_data(df_defense_short)
        else:  # If at least one played is selected
            # Display data for the selected player(s)
            df_defense_short = df_defense[df_defense.player.isin(selected_player)]
            return defense_player_data(df_defense_short)

    if attribute_value is None:  # If no minimum number of playing time (in minutes_90s) is given
        return defense_update_table(attribute, attribute_value, selected_team, selected_player, df_defense)
    else:  # If a minimum number of playing time (in minutes_90s) is given
        return defense_update_table(attribute, attribute_value, selected_team, selected_player, df_defense)


# Callback 5 - Display table shape statistics
@callback(
    dash.dependencies.Output('defense_player_search_dataframe_shape', "children"), [
        dash.dependencies.Input("defense_player_search_select_attribute", "value"),
        dash.dependencies.Input('defense_player_search_attribute_input', "value"),
        dash.dependencies.Input("defense_player_search_select_team", 'value'),
        dash.dependencies.Input("defense_player_search_select_player", 'value'),
    ])
def defense_player_search_table_shape(attribute, attribute_value, selected_team, selected_player):
    if not selected_team:
        df_defense_selectable = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
        df_defense_selected = df_defense[df_defense.player.isin(selected_player)]
        return (f'Number of available players to choose from: {df_defense_selectable.shape[0]}',
                html.Br(),
                f'Number of selected players: {df_defense_selected.shape[0]}',
                html.Br(),
                f'Number of attributes: {df_defense_selected.shape[1]}')
    else:
        try:
            df_defense_selectable = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
        except KeyError:
            df_defense_selectable = df_defense
        df_defense_selectable = df_defense_selectable[df_defense_selectable.team.isin(selected_team)]
        df_defense_selected = df_defense[df_defense.player.isin(selected_player)]
        return (f'Number of available players to choose from: {df_defense_selectable.shape[0]}',
                html.Br(),
                f'Number of selected players: {df_defense_selected.shape[0]}',
                html.Br(),
                f'Number of attributes: {df_defense_selected.shape[1]}')


# 2. Section for part-to-whole (Pie Chart + Bar Chart)
# Callback 1 - Input menu based on selected attribute to filter on
@callback(
    dash.dependencies.Output('defense_pie-chart_attribute_input_div', 'children'), [
        dash.dependencies.Input("defense_pie-chart_select_attribute", "value")
    ])
def defense_player_attribute_input(attribute):
    try:
        return html.Div([
            html.B(f"Minimum number of {attribute}:"),
            html.Br(),
            dcc.Input(
                id='defense_pie-chart_attribute_input',
                type='number', min=0, max=df_defense[attribute].max(),
                placeholder=f"Range: 0-{df_defense[attribute].max()}",
                debounce=True)
        ])
    except KeyError:
        return None  # don't return any text


# Callback 2 - Split into age brackets and plot pie chart
@callback(
    dash.dependencies.Output('defense_pie-chart', 'figure'), [
        dash.dependencies.Input('defense_pie-chart_brackets_input', 'value'),
        dash.dependencies.Input("defense_pie-chart_select_attribute", "value"),
        dash.dependencies.Input('defense_pie-chart_attribute_input', "value")
    ], prevent_initial_call=True)
def defense_pie_chart_bracket_split(n_brackets, attribute, attribute_value):
    try:
        df_defense_short = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
        df_bracket = defense_extract_age_bracket_pie_chart(n_brackets, df_defense_short)
        fig = px.pie(df_bracket, values='Count', names='Bracket', hover_data=['Percent'], title='Age Bracket Pie Chart',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    except ValueError:  # If n_brackets is not set
        return {}  # return empty figure


# Callback 3 - Split into age brackets and plot bar chart
@callback(
    dash.dependencies.Output('defense_barchart', 'figure'), [
        dash.dependencies.Input('defense_pie-chart_brackets_input', 'value'),
        dash.dependencies.Input("defense_pie-chart_select_attribute", "value"),
        dash.dependencies.Input('defense_pie-chart_attribute_input', "value")
    ], prevent_initial_call=True)
def defense_barchart_bracket_split(n_brackets, attribute, attribute_value):
    try:
        df_defense_short = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
        df_bracket = defense_extract_age_bracket_pie_chart(n_brackets, df_defense_short)
        fig = px.bar(df_bracket, x='Bracket', y='Count', hover_data=['Percent'], title='Age Bracket Bar Chart',
                     text_auto='.2s')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        return fig
    except ValueError:  # If n_brackets is not set
        return {}  # return empty figure


# Callback 4 - Print total number of players
@callback(
    dash.dependencies.Output('defense_pie-chart_brackets_text', 'children'), [
        dash.dependencies.Input("defense_pie-chart_select_attribute", "value"),
        dash.dependencies.Input('defense_pie-chart_attribute_input', "value")
    ], prevent_initial_call=True)
def defense_pie_chart_barchart_entries(attribute, attribute_value):
    df_defense_short = df_defense.drop(df_defense[df_defense[attribute] <= attribute_value].index)
    return f'Total number of players: {df_defense_short.shape[0]}'


# 3. Section for distribution plots (violin plot and bar charts)
# Callback 1 - Update violin plot based on selected y-axis attribute and number of brackets
@callback(
    dash.dependencies.Output('defense_violin_plot', 'figure'), [
        dash.dependencies.Input("defense_distribution_attribute_input", 'value'),
        dash.dependencies.Input('defense_distribution_brackets_input', 'value'),
        dash.dependencies.Input('defense_distribution_equal_split_switch', 'on'),
        dash.dependencies.Input('defense_distribution_matches_input', 'value'),
    ], prevent_initial_call=True)
def defense_violin_plot_update(y_attribute, n_brackets, equal_division, n_matches):
    try:
        return defense_update_violin_plot(y_attribute, n_brackets, equal_division, n_matches)
    except (KeyError, TypeError):  # If y_attribute or n_brackets is not set
        return {}  # return empty figure


# Callback 2 - Update left bar chart based on selected y-axis attribute and number of brackets
@callback(
    dash.dependencies.Output('defense_distribution_bar_chart_matches', 'figure'), [
        dash.dependencies.Input("defense_distribution_attribute_input", 'value'),
        dash.dependencies.Input('defense_distribution_brackets_input', 'value'),
        dash.dependencies.Input('defense_distribution_equal_split_switch', 'on'),
        dash.dependencies.Input('defense_distribution_matches_input', 'value'),
    ], prevent_initial_call=True)
def defense_distribution_bar_chart_matches_update(y_attribute, n_brackets, equal_division, n_matches):
    try:
        df_bracket_averages = (
            defense_update_distribution_bar_chart(y_attribute, n_brackets, equal_division, n_matches))

        # Make bar chart
        fig = px.bar(df_bracket_averages, x='Bracket', y=f'{y_attribute} / # matches',
                     title=f'Average "{y_attribute}" per match played by all players in an age bracket',
                     text_auto='.2s', hover_data=['Number of players', f'Sum of {y_attribute} over all players',
                                                  'Number of matches played over all players'])
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        return fig
    except (KeyError, TypeError, ValueError):  # If y_attribute or n_brackets is not set
        return {}  # return empty figure


# Callback 3 - Update right bar chart based on selected y-axis attribute and number of brackets
@callback(
    dash.dependencies.Output('defense_distribution_bar_chart_entries', 'figure'), [
        dash.dependencies.Input("defense_distribution_attribute_input", 'value'),
        dash.dependencies.Input('defense_distribution_brackets_input', 'value'),
        dash.dependencies.Input('defense_distribution_equal_split_switch', 'on'),
        dash.dependencies.Input('defense_distribution_matches_input', 'value'),
    ], prevent_initial_call=True)
def defense_distribution_bar_chart_entries_update(y_attribute, n_brackets, equal_division, n_matches):
    try:
        df_bracket_averages = (
            defense_update_distribution_bar_chart(y_attribute, n_brackets, equal_division, n_matches))

        # Make bar chart
        fig = px.bar(df_bracket_averages, x='Bracket', y=f'{y_attribute} / # players',
                     title=f'Average "{y_attribute}" per player in an age bracket (mean)',
                     text_auto='.2f', hover_data=['Number of players', f'Sum of {y_attribute} over all players',
                                                  'Number of matches played over all players'])
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        return fig
    except (KeyError, TypeError, ValueError):  # If y_attribute or n_brackets is not set
        return {}  # return empty figure


# Callback 4 - Switch to show the (hover)data in table or not
@callback(
    dash.dependencies.Output('defense_distribution_hovertext_output_div', 'style'), [
        dash.dependencies.Input('defense_distribution_show_hoverdata_switch', 'on')
    ])
def defense_multi_scatterplot_show_bracket_dropdown(show_hoverdata):
    if show_hoverdata is True:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# Callback 5 - Display (hover)data in table
@callback(
    dash.dependencies.Output('defense_distribution_table', 'children'), [
        dash.dependencies.Input("defense_distribution_attribute_input", 'value'),
        dash.dependencies.Input('defense_distribution_brackets_input', 'value'),
        dash.dependencies.Input('defense_distribution_equal_split_switch', 'on'),
        dash.dependencies.Input('defense_distribution_matches_input', 'value'),
    ])
def defense_distribution_bar_chart_entries_update(y_attribute, n_brackets, equal_division, n_matches):
    try:
        df_bracket_averages = (
            defense_update_distribution_bar_chart(y_attribute, n_brackets, equal_division, n_matches))

        return dash_table.DataTable(
            data=df_bracket_averages.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df_bracket_averages.columns],
            style_table={'overflowY': 'scroll', 'maxHeight': '420px'}
        )
    except (KeyError, TypeError, AttributeError):  # If y_attribute or n_brackets is not set
        return None  # return empty text


# 4. Section for multi scatterplot
# Callback 1 - Show the dropdown menu for changing brackets if 'Bracket' is selected
@callback(
    dash.dependencies.Output('defense_multi_scatterplot_brackets_input_div', 'style'), [
        dash.dependencies.Input("defense_multi_scatterplot_multiple_type_input", 'value')
    ])
def defense_multi_scatterplot_show_bracket_dropdown(filter_type):
    if filter_type == 'Bracket':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# Callback 2 - Show the dropdown menu for changing teams if 'Team' is selected
@callback(
    dash.dependencies.Output("defense_multi_scatterplot_teams_input_div", 'style'), [
        dash.dependencies.Input("defense_multi_scatterplot_multiple_type_input", 'value')
    ])
def defense_multi_scatterplot_show_team_dropdown(filter_type):
    if filter_type == 'Team':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# Callback 3 - Limit number of selected teams to 5
@callback(
    dash.dependencies.Output("defense_multi_scatterplot_teams_input", 'options'), [
        dash.dependencies.Input("defense_multi_scatterplot_teams_input", 'value')
    ], prevent_initial_call=True)
def defense_multi_scatterplot_limit_team_selection(teams):
    OPTIONS = [{"label": i, "value": i} for i in sorted(df_defense['team'].unique())]
    if len(teams) == 5:
        return [option for option in OPTIONS if option['value'] in teams]
    else:
        return OPTIONS


# Callback 4 - Update the multi scatterplot based on the input
@callback(
    dash.dependencies.Output('defense_multi_scatterplot', 'figure'), [
        dash.dependencies.Input("defense_multi_scatterplot_attribute_input", 'value'),
        dash.dependencies.Input('defense_multi_scatterplot_brackets_input', 'value'),
        dash.dependencies.Input("defense_multi_scatterplot_teams_input", 'value'),
        dash.dependencies.Input('defense_multi_scatterplot_equal_split_switch', 'on'),
        dash.dependencies.Input('defense_multi_scatterplot_matches_input', 'value'),
    ])
def defense_multi_scatterplot_update(y_attribute, n_brackets, selected_teams, equal_division, n_matches):
    # Drop players with fewer matches than the input 'n_matches'
    df_defense_matches = df_defense.drop(df_defense[df_defense['minutes_90s'] <= n_matches].index)

    try:
        return defense_update_multi_scatterplot(y_attribute, n_brackets, selected_teams, equal_division,
                                                df_defense_matches)
    except (KeyError, TypeError):  # If y_attribute or n_brackets is not set
        return {}  # return empty figure


# Callback 5 - Display number of data points used per fit line/sub-scatterplot
@callback(
    dash.dependencies.Output("defense_multi_scatterplot_entries_text", 'children'), [
        dash.dependencies.Input("defense_multi_scatterplot_attribute_input", 'value'),
        dash.dependencies.Input('defense_multi_scatterplot_brackets_input', 'value'),
        dash.dependencies.Input("defense_multi_scatterplot_teams_input", 'value'),
        dash.dependencies.Input('defense_multi_scatterplot_equal_split_switch', 'on'),
        dash.dependencies.Input('defense_multi_scatterplot_matches_input', 'value'),
    ])
def defense_multi_scatterplot_count(y_attribute, n_brackets, selected_teams, equal_division, n_matches):
    # Drop players with fewer matches than the input 'n_matches'
    df_defense_matches = df_defense.drop(df_defense[df_defense['minutes_90s'] <= n_matches].index)

    try:
        return defense_count_multi_scatterplot(y_attribute, n_brackets, selected_teams, equal_division,
                                               df_defense_matches)
    except (KeyError, TypeError):  # If y_attribute or n_brackets is not set
        return {}  # return empty figure


# Callback 6 - Display correlation per fit line/sub-scatterplot
@callback(
    dash.dependencies.Output("defense_multi_scatterplot_correlation_text", 'children'), [
        dash.dependencies.Input("defense_multi_scatterplot_attribute_input", 'value'),
        dash.dependencies.Input('defense_multi_scatterplot_brackets_input', 'value'),
        dash.dependencies.Input("defense_multi_scatterplot_teams_input", 'value'),
        dash.dependencies.Input('defense_multi_scatterplot_equal_split_switch', 'on'),
        dash.dependencies.Input('defense_multi_scatterplot_matches_input', 'value'),
    ])
def defense_multi_scatterplot_count(y_attribute, n_brackets, selected_teams, equal_division, n_matches):
    # Drop players with fewer matches than the input 'n_matches'
    df_defense_matches = df_defense.drop(df_defense[df_defense['minutes_90s'] <= n_matches].index)

    try:
        return defense_correlation_multi_scatterplot(y_attribute, n_brackets, selected_teams, equal_division,
                                                     df_defense_matches)
    except (KeyError, TypeError):  # If y_attribute or n_brackets is not set
        return {}  # return empty figure
