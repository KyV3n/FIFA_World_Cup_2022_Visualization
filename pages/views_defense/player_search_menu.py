from dash import dcc, html

from pages.views_defense.config import *


def generate_description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="defense_player_search_card",
        children=[
            html.H5("Player Search"),
            html.Div(
                id="defense_player_search_card_text",
                children="Search for players or filter to find players to compare their raw data statistics."
                         "A dictionary for all attributes can be found at the bottom of this page",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    team_list = sorted(df_defense['team'].unique())
    return html.Div(
        id="defense_player_search_control_card",
        children=[
            html.Br(),
            html.B("Attribute to filter on:"),
            dcc.Dropdown(
                id="defense_player_search_select_attribute",
                options=[{"label": i, "value": i} for i in attribute_list_2],
                value='minutes_90s'
            ),

            html.Div(
                id='defense_player_search_attribute_input_div',
                children=[
                    dcc.Input(
                        id='defense_player_search_attribute_input',
                        type='number',
                        min=0,
                        debounce=True
                    )
                ]
            ),

            html.Br(),
            html.B("Team:"),
            dcc.Dropdown(
                id="defense_player_search_select_team",
                options=[{"label": team, "value": team} for team in team_list],
                value=[],
                multi=True
            ),

            html.Br(),
            html.B("Player:"),
            dcc.Dropdown(
                id="defense_player_search_select_player",
                value=[],
                multi=True
            ),

            html.Br(),
            html.Div(id='defense_player_search_dataframe_shape')
        ], style={"textAlign": "float-left"}
    )


def defense_make_menu_layout_player_search():
    return [generate_description_card(), generate_control_card()]
