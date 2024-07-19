import os
import tomllib
from pathlib import Path
from typing import Dict

import pandas as pd
import requests

__all__ = ['datasets', 'datasets_label']


class DataProvider:
    config_file = Path(__file__).parent.parent / 'app_config.toml'
    data_api_hello_endpoint = '{api_server}/api/v1'
    data_api_endpoints_base = {
        'housing_data': '{api_server}/api/v1/dataset/housing',
        'travel_data': '{api_server}/api/v1/dataset/travel',
        'lm_data': '{api_server}/api/v1/dataset/labour-market',
    }

    def __init__(self) -> None:
        self.__datasets: Dict[str, pd.DataFrame] = {}

        self.__load_data()
        self.__preprocess_data()

    @property
    def datasets(self) -> Dict[str, pd.DataFrame]:
        return self.__datasets

    def _load_api_server_url(self) -> str:
        if 'BACKEND_SERVER_URL' in os.environ:
            return os.environ['BACKEND_SERVER_URL']

        if self.config_file.exists():
            with open(self.config_file, 'rb') as fb:
                config = tomllib.load(fb)
        else:
            raise FileNotFoundError("App Start Failed: Config file not found")

        if 'api_server' not in config:
            raise ValueError("App Start Failed: Missing API Server configuration")

        return config['api_server']

    def __load_datasets(self, api_server) -> None:
        try:
            response = requests.get(self.data_api_hello_endpoint.format(api_server=api_server))
            response.raise_for_status()
        except requests.RequestException:
            raise requests.RequestException(
                f"App Start Failed: Cannot connect to API Server at {api_server}"
            )

        data_api_endpoints = {
            dataset: url.format(api_server=api_server)
            for dataset, url in self.data_api_endpoints_base.items()
        }

        for dataset, url in data_api_endpoints.items():
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException:
                raise requests.RequestException(
                    f"App Start Failed: Cannot fetch data from {url}"
                )

            self.__datasets[dataset] = pd.DataFrame(
                requests.get(row['uri']).json() for row in response.json()
            )

    def __load_data(self) -> None:
        try:
            api_server = self._load_api_server_url()
            self.__load_datasets(api_server)
        except (FileNotFoundError, ValueError, requests.RequestException) as e:
            print(e)
            exit(1)

    def __preprocess_data(self) -> None:
        self.__datasets['lm_data'].rename(columns={
            'quarter_mid_y': 'year',
            'quarter_mid_m': 'month',
        }, inplace=True)

        self.__datasets['travel_data']['annual_growth_bus'] = (
            self.__datasets['travel_data']['bus_journeys'].pct_change(13)
        )
        self.__datasets['travel_data']['annual_growth_tube'] = (
            self.__datasets['travel_data']['tube_journeys'].pct_change(13)
        )

        self.__datasets['lm_data']['annual_growth_ldn'] = (
            self.__datasets['lm_data']['unemployment_rate_ldn'].pct_change(12)
        )
        self.__datasets['lm_data']['annual_growth_uk'] = (
            self.__datasets['lm_data']['unemployment_rate_uk'].pct_change(12)
        )

        self.__datasets['travel_data']['total_journeys'] = (
                self.__datasets['travel_data']['bus_journeys'] + self.__datasets['travel_data']['tube_journeys']
        )
        self.__datasets['travel_data']['annual_growth_total'] = (
            self.__datasets['travel_data']['total_journeys'].pct_change(13)
        )


datasets: Dict[str, pd.DataFrame] = DataProvider().datasets
datasets_label = {
    'housing_data': 'Housing Data',
    'travel_data': 'Travel Data',
    'lm_data': 'Labour Market Data',
}
