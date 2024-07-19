import datetime
from typing import Tuple

import pandas as pd

__linear_graph_types = ('line', 'bar')


def __housing_linear(dataframe: pd.DataFrame, graph_type: str, is_value: bool = True) -> dict:
    return {
        'data': [
            {
                'x': dataframe['year'].unique(),
                'y': dataframe[
                    'value_ldn' if is_value else 'annual_growth_ldn'
                ][dataframe['month'] == month],
                'type': graph_type,
                'name': f'{datetime.date(1990, month, 1).strftime("%B")}'
            } for month in dataframe['month'].unique()
        ],
        'layout': {
            'title': 'London House Price' if is_value else 'London House Price Trends',
            'xaxis': {'title': 'Year', 'dtick': max(dataframe['year'].nunique() // 8, 1)},
            'yaxis': {'title': 'Price' if is_value else 'Annual Growth'},
        },
    }


def __travel_linear(dataframe: pd.DataFrame, graph_type: str, is_value: bool = True) -> dict:
    return {
        'data': [
            {
                'x': dataframe['year'].unique(),
                'y': dataframe[
                    'total_journeys' if is_value else 'annual_growth_total'
                ][dataframe['period'] == period],
                'type': graph_type,
                'name': f'Period {period}'
            } for period in dataframe['period'].unique()
        ],
        'layout': {
            'title': 'London Travel Journey' if is_value else 'London Travel Journey Trends',
            'xaxis': {'title': 'Year', 'dtick': max(dataframe['year'].nunique() // 8, 1)},
            'yaxis': {'title': 'Journeys' if is_value else 'Annual Growth'},
        },
    }


def __lm_linear(dataframe: pd.DataFrame, graph_type: str, is_value: bool = True) -> dict:
    return {
        'data': [
            {
                'x': dataframe['year'].unique(),
                'y': dataframe[
                    'unemployment_rate_ldn' if is_value else 'annual_growth_ldn'
                ][dataframe['month'] == month],
                'type': graph_type,
                'name': f'{datetime.date(1990, month, 1).strftime("%B")}'
            } for month in dataframe['month'].unique()
        ],
        'layout': {
            'title': 'London Unemployment Rate' if is_value else 'London Unemployment Rate Trends',
            'xaxis': {'title': 'Year', 'dtick': max(dataframe['year'].nunique() // 8, 1)},
            'yaxis': {'title': 'Unemployment Rate' if is_value else 'Annual Growth'},
        },
    }


def __housing_heatmap(dataframe: pd.DataFrame, is_value: bool = True) -> dict:
    x_label = dataframe['year'].unique()
    y_label = dataframe['month'].unique()

    data_mat = []
    for month in y_label:
        row = []
        for year in x_label:
            value = dataframe[
                'value_ldn' if is_value else 'annual_growth_ldn'
            ][(dataframe['year'] == year) & (dataframe['month'] == month)]
            row.append(value.values[0] if not value.empty else None)
        data_mat.append(row)

    fig = {
        'data': [{
            'z': data_mat,
            'x': x_label,
            'y': [datetime.date(1990, month, 1).strftime("%B") for month in y_label],
            'type': 'heatmap',
            'colorscale': 'Viridis' if is_value else 'RdBu',
        }],
        'layout': {
            'title': 'London House Price' if is_value else 'London House Price Trends',
            'xaxis': {'title': 'Year'},
        },
    }

    return fig


def __travel_heatmap(dataframe: pd.DataFrame, is_value: bool = True) -> dict:
    x_label = dataframe['year'].unique()
    y_label = dataframe['period'].unique()

    data_mat = []
    for period in y_label:
        row = []
        for year in x_label:
            value = dataframe[
                'total_journeys' if is_value else 'annual_growth_total'
            ][(dataframe['year'] == year) & (dataframe['period'] == period)]
            row.append(value.values[0] if not value.empty else None)
        data_mat.append(row)

    fig = {
        'data': [{
            'z': data_mat,
            'x': x_label,
            'y': [f'Period {period}' for period in y_label],
            'type': 'heatmap',
            'colorscale': 'Viridis' if is_value else 'RdBu',
        }],
        'layout': {
            'title': 'London Travel Journey' if is_value else 'London Travel Journey Trends',
            'xaxis': {'title': 'Year'},
        },
    }

    return fig


def _lm_heatmap(dataframe: pd.DataFrame, is_value: bool = True) -> dict:
    x_label = dataframe['year'].unique()
    y_label = dataframe['month'].unique()

    data_mat = []
    for month in y_label:
        row = []
        for year in x_label:
            value = dataframe[
                'unemployment_rate_ldn' if is_value else 'annual_growth_ldn'
            ][(dataframe['year'] == year) & (dataframe['month'] == month)]
            row.append(value.values[0] if not value.empty else None)
        data_mat.append(row)

    fig = {
        'data': [{
            'z': data_mat,
            'x': x_label,
            'y': [datetime.date(1990, month, 1).strftime("%B") for month in y_label],
            'type': 'heatmap',
            'colorscale': 'Viridis' if is_value else 'RdBu',
        }],
        'layout': {
            'title': 'London Unemployment Rate' if is_value else 'London Unemployment Rate Trends',
            'xaxis': {'title': 'Year'},
        },
    }

    return fig


def compose_housing_graph(
        dataframe: pd.DataFrame, value_graph_type: str, trends_graph_type: str,
) -> Tuple[dict, dict]:
    return (
        __housing_linear(dataframe, value_graph_type, is_value=True)
        if value_graph_type in __linear_graph_types
        else __housing_heatmap(dataframe, is_value=True)
    ), (
        __housing_linear(dataframe, trends_graph_type, is_value=False)
        if trends_graph_type in __linear_graph_types
        else __housing_heatmap(dataframe, is_value=False)
    )


def compose_travel_graph(
        dataframe: pd.DataFrame, value_graph_type: str, trends_graph_type: str,
) -> Tuple[dict, dict]:
    return (
        __travel_linear(dataframe, value_graph_type, is_value=True)
        if value_graph_type in __linear_graph_types
        else __travel_heatmap(dataframe, is_value=True)
    ), (
        __travel_linear(dataframe, trends_graph_type, is_value=False)
        if trends_graph_type in __linear_graph_types
        else __travel_heatmap(dataframe, is_value=False)
    )


def compose_lm_graph(
        dataframe: pd.DataFrame, value_graph_type: str, trends_graph_type: str,
) -> Tuple[dict, dict]:
    return (
        __lm_linear(dataframe, value_graph_type, is_value=True)
        if value_graph_type in __linear_graph_types
        else _lm_heatmap(dataframe, is_value=True)
    ), (
        __lm_linear(dataframe, trends_graph_type, is_value=False)
        if trends_graph_type in __linear_graph_types
        else _lm_heatmap(dataframe, is_value=False)
    )
