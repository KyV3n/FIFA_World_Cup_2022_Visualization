from dash import dcc, html
from ..views_defense.config import *
import dash_daq as daq


def generate_description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="defense_distribution_card",
        children=[
            html.H5("Distribution plots"),
            html.Div(
                id="defense_distribution_card_text",
                children="Shows violin plots and bar charts, which can be used to find differences in distribution "
                         "between age brackets, based on any attribute for the y-axis. "
                         "The right bar chart takes into account the number of players per bracket "
                         "and the left bar chart is adjusted to take into account the number of matches all players "
                         "in a bracket have played in total."
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="defense_distribution_control_card",
        children=[
            html.Br(),
            html.B("Minimum matches (90 minutes) played, can be float value:"),
            dcc.Input(
                id='defense_distribution_matches_input',
                type='number', min=0, max=7.7,
                placeholder="Range: 0-7.7",
                debounce=True,
                value=0,
            ),

            html.Br(),
            html.Br(),
            html.B("Attribute on y-axis:"),
            dcc.Dropdown(
                id="defense_distribution_attribute_input",
                options=[{"label": i, "value": i} for i in attribute_list],
                value='minutes_90s'
            ),

            html.Br(),
            html.B("Number of age brackets to be split:"),
            dcc.Input(
                id='defense_distribution_brackets_input',
                type='number', min=2, max=5, step=1,
                placeholder="Range: 2-5",
                debounce=False
            ),

            html.Br(),
            html.B("Equal division of number of items per age bracket?:"),
            daq.BooleanSwitch(
                id='defense_distribution_equal_split_switch',
                on=False
            ),

            html.Br(),
            html.Br(),
            html.B("Show (hover)data in table below?:"),
            daq.BooleanSwitch(
                id='defense_distribution_show_hoverdata_switch',
                on=True
            ),

            html.Div([
                html.Br(),
                html.Div(id='defense_distribution_table')
            ], id='defense_distribution_hovertext_output_div')

        ], style={"textAlign": "float-left"}
    )


def defense_make_menu_layout_distribution_plot():
    return [generate_description_card(), generate_control_card()]
