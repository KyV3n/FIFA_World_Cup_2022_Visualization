from dash import dcc, html
from ..views_defense.config import *
import dash_daq as daq


def generate_description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="defense_scatterplot_card",
        children=[
            html.H5("Scatterplot with fit lines"),
            html.Div(
                id="defense_scatterplot_card_text",
                children="A scatterplot with fit line, which can be used to find correlation between age on the x-axis"
                         " and any other freely chosen attribute on the y-axis. "
                         "It is also possible to split the scatterplot points into multiple subsets based on either "
                         "age brackets or teams. Multiple fit lines will then be shown.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="defense_scatterplot_control_card",
        children=[
            html.Br(),
            html.B("Minimum matches (90 minutes) played, can be float value:"),
            dcc.Input(
                id='defense_multi_scatterplot_matches_input',
                type='number', min=0, max=7.7,
                placeholder="Range: 0-7.7",
                debounce=True,
                value=0,
            ),

            html.Br(),
            html.Br(),
            html.B("Attribute on y-axis:"),
            dcc.Dropdown(
                id="defense_multi_scatterplot_attribute_input",
                options=[{"label": i, "value": i} for i in attribute_list],
                value='minutes_90s'
            ),

            html.Br(),
            html.B("Split on age brackets or teams?:"),
            dcc.Dropdown(
                id="defense_multi_scatterplot_multiple_type_input",
                options=[{"label": i, "value": i} for i in ['Bracket', 'Team']],
                value='minutes_90s'
            ),

            html.Div([
                html.Br(),
                html.B("Number of age brackets to be split:"),
                dcc.Input(
                    id='defense_multi_scatterplot_brackets_input',
                    type='number', min=2, max=5, step=1,
                    placeholder="Range: 2-5",
                    debounce=False),

                html.Br(),
                html.B("Equal division of number of items per age bracket?:"),
                daq.BooleanSwitch(
                    id='defense_multi_scatterplot_equal_split_switch',
                    on=False),
            ], id='defense_multi_scatterplot_brackets_input_div'),

            html.Div([
                html.Br(),
                html.B("Teams:"),
                dcc.Dropdown(
                    id="defense_multi_scatterplot_teams_input",
                    options=[{"label": i, "value": i} for i in sorted(df_defense['team'].unique())],
                    multi=True, placeholder='Select a maximum of 5', value=[]),
            ], id="defense_multi_scatterplot_teams_input_div"),

            html.Br(),
            html.Div(id="defense_multi_scatterplot_entries_text"),
            html.Br(),
            html.Div(id="defense_multi_scatterplot_correlation_text"),
        ], style={"textAlign": "float-left"}
    )


def defense_make_menu_layout_multi_scatterplot():
    return [generate_description_card(), generate_control_card()]
