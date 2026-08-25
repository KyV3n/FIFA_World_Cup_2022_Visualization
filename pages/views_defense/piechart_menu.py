from dash import dcc, html
from ..views_defense.config import *


def generate_description_card():
    """
    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="defense_pie-chart_card",
        children=[
            html.H5("Part-to-whole"),
            html.Div(
                id="defense_pie-chart_card_text",
                children="Filter on any attribute and the number of age brackets. A pie chart and bar chart will "
                         "then be shown, which will help to understand the part-to-whole relationship for the "
                         "number of players per age bracket.",
            ),
        ],
    )


def generate_control_card():
    """
    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="defense_pie-chart_control_card",
        children=[
            html.Br(),
            html.B("Attribute to filter on:"),
            dcc.Dropdown(
                id="defense_pie-chart_select_attribute",
                options=[{"label": i, "value": i} for i in attribute_list_2],
                value='minutes_90s'
            ),

            html.Br(),
            html.Div(id='defense_pie-chart_attribute_input_div'),

            html.Br(),
            html.B("Number of age brackets to be split:"),
            dcc.Input(
                id='defense_pie-chart_brackets_input',
                type='number', min=2, max=10, step=1,
                placeholder="Range: 2-10",
                debounce=False
            ),

            html.Br(),
            html.Br(),
            html.Div(id='defense_pie-chart_brackets_text')
        ], style={"textAlign": "float-left"}
    )


def defense_make_menu_layout_pie_chart():
    return [generate_description_card(), generate_control_card()]
