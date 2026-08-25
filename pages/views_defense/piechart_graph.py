import pandas as pd
from dash import dcc, html


def defense_plot_pie_bar_chart():
    return html.Div(
        id="defense_pie-chart_graph_object",
        children=[
            dcc.Graph(id='defense_pie-chart', className="six columns"),
            dcc.Graph(id='defense_barchart', className='six columns')
        ],
    )


def defense_extract_age_bracket_pie_chart(n_brackets, df_defense):
    """
    Extracts information about the number of players inside each age bracket.
    :param n_brackets: selected number of brackets to be split in
    :param df_defense: defense DataFrame
    :return: DataFrame containing count and percent of each age bracket for part-to-whole
    """
    def round_integer(x):
        """
        Rounds float number up and down to the lowest integer
        :param x: float number
        :return: nearest integer
        """
        i, f = divmod(x, 1)
        return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

    if n_brackets is not None:
        # Change lowest/highest age dynamically with the minimum number of matches played (different brackets)
        # highest_age = int(df_defense['age_years'].max()) + 1
        # lowest_age = int(df_defense['age_years'].min())

        # Stationary lowest/highest age dynamically with the minimum number of matches played (brackets do not change)
        highest_age = 40
        lowest_age = 19

        # Initialize variables for bracket split
        part_length = (highest_age - lowest_age) / n_brackets
        parts = []
        marker = lowest_age

        # Age bracket split
        for _ in range(n_brackets):
            part = [round_integer(marker), round_integer(marker + part_length)]
            marker += part_length
            parts.append(part)

        # Put the number of entries for each age bracket and it's percent as part-to-whole in a DataFrame
        bracket_sum_list = []
        for i in range(len(parts)):
            lower = parts[i][0]
            higher = parts[i][1]

            in_bracket = df_defense['age_float'].between(lower, higher)
            sum_entries_bracket = in_bracket.values.sum()
            percent_of_whole = round((sum_entries_bracket / len(df_defense.index) * 100), 2)
            bracket_sum = {'Bracket': f'{lower}-{higher}', 'Count': sum_entries_bracket, 'Percent': percent_of_whole}

            bracket_sum_list.append(bracket_sum)

        df_bracket = pd.DataFrame.from_dict(bracket_sum_list)
        return df_bracket
