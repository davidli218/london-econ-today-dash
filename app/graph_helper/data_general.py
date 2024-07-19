from typing import Tuple

import pandas as pd


def general_housing_graph(
        dataframe: pd.DataFrame, value_graph_type: str, trends_graph_type: str
) -> Tuple[dict, dict]:
    x_label = dataframe['year'].astype(str) + '-' + dataframe['month'].astype(str)

    fig_value = {
        'data': [
            {
                'x': x_label,
                'y': dataframe['value_ldn'],
                'type': value_graph_type,
                'name': 'London',
            },
            {
                'x': x_label,
                'y': dataframe['value_uk'],
                'type': value_graph_type,
                'name': 'UK',
            },
        ],
        'layout': {
            'title': 'House Price',
            'xaxis': {'title': 'Year-Month'},
            'yaxis': {'title': 'Price'},
        },
    }

    fig_trends = {
        'data': [
            {
                'x': x_label,
                'y': dataframe['annual_growth_ldn'],
                'type': trends_graph_type,
                'name': 'London',
            },
            {
                'x': x_label,
                'y': dataframe['annual_growth_uk'],
                'type': trends_graph_type,
                'name': 'UK',
            },
        ],
        'layout': {
            'title': 'House Price Trends',
            'xaxis': {'title': 'Year-Month'},
            'yaxis': {'title': 'Annual Growth'},
        },
    }

    return fig_value, fig_trends


def general_travel_graph(
        dataframe: pd.DataFrame, value_graph_type: str, trends_graph_type: str
) -> Tuple[dict, dict]:
    x_label = dataframe['year'].astype(str) + ' #' + dataframe['period'].astype(str)

    fig_value = {
        'data': [
            {
                'x': x_label,
                'y': dataframe['bus_journeys'],
                'type': value_graph_type,
                'name': 'Bus',
            },
            {
                'x': x_label,
                'y': dataframe['tube_journeys'],
                'type': value_graph_type,
                'name': 'Tube',
            },
        ],
        'layout': {
            'title': 'Travel Journeys',
            'xaxis': {'title': 'Year #Period'},
            'yaxis': {'title': 'Journeys'},
        },
    }

    fig_trends = {
        'data': [
            {
                'x': x_label,
                'y': dataframe['annual_growth_bus'],
                'type': trends_graph_type,
                'name': 'Bus',
            },
            {
                'x': x_label,
                'y': dataframe['annual_growth_tube'],
                'type': trends_graph_type,
                'name': 'Tube',
            },
        ],
        'layout': {
            'title': 'Travel Journeys Trends',
            'xaxis': {'title': 'Year #Period'},
            'yaxis': {'title': 'Annual Growth'},
        },
    }

    return fig_value, fig_trends


def general_lm_graph(
        dataframe: pd.DataFrame, value_graph_type: str, trends_graph_type: str,
) -> Tuple[dict, dict]:
    x_label = dataframe['year'].astype(str) + '-' + dataframe['month'].astype(str)

    fig_value = {
        'data': [
            {
                'x': x_label,
                'y': dataframe['unemployment_rate_ldn'],
                'type': value_graph_type,
                'name': 'London',
            },
            {
                'x': x_label,
                'y': dataframe['unemployment_rate_uk'],
                'type': value_graph_type,
                'name': 'UK',
            },
        ],
        'layout': {
            'title': 'Unemployment Rate',
            'xaxis': {'title': 'Year-Month'},
            'yaxis': {'title': 'Unemployment Rate'},
        },
    }

    fig_trends = {
        'data': [
            {
                'x': x_label,
                'y': dataframe['annual_growth_ldn'],
                'type': trends_graph_type,
                'name': 'London',
            },
            {
                'x': x_label,
                'y': dataframe['annual_growth_uk'],
                'type': trends_graph_type,
                'name': 'UK',
            },
        ],
        'layout': {
            'title': 'Unemployment Rate Trends',
            'xaxis': {'title': 'Year-Month'},
            'yaxis': {'title': 'Annual Growth'},
        },
    }

    return fig_value, fig_trends
