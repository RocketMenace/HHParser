from abc import ABC, abstractmethod
from typing import Any
import requests
from loguru import logger
from requests.exceptions import HTTPError


class BaseAPIManager(ABC):

    @abstractmethod
    def api_connection(self):
        pass


class BaseApiConnector(ABC):

    @abstractmethod
    def _get_data(self) -> list[dict]:
        pass


class APIManager(BaseAPIManager):
    """API connection manager."""

    def __init__(self, connector):
        self.connector = connector

    def api_connection(self):
        """Connects to API using specified API connector."""
        content = self.connector._get_data()
        return content


class HHApiConnector(BaseApiConnector):
    """API connector for extracting data form hh.ru"""
    _url: str = "https://api.hh.ru/vacancies"
    _headers: dict[str, str] = {"User-Agent": "api-test-agent"}
    _params: dict[str, Any] = {"text": " ", "page": 0, "per_page": 100}

    def __init__(self):
        self.vacancies = []

    def _get_data(self) -> list[dict]:
        """Extract data using specified parameters."""
        keyword = "Программист"
        HHApiConnector._params["text"] = keyword.title()
        employers_id = ['5124731',
                        '907345',
                        "239363",
                        "4813742",
                        "5060211",
                        "78638",
                        "80",
                        "3529",
                        "1740",
                        "41144",
                        "4118",
                        "6093775",
                        "39305"]
        HHApiConnector._params["employer_id"] = employers_id
        while HHApiConnector._params.get("page") != 20:
            try:
                response = requests.get(
                    url=HHApiConnector._url, params=HHApiConnector._params, timeout=90
                )
                response.raise_for_status()
                vacancies = response.json()["items"]
                self.vacancies.extend(vacancies)
                HHApiConnector._params["page"] += 1

            except HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                logger.add(
                    "../errors_logs/errors.log",
                    level="ERROR",
                    format="{time} {level} {message}",
                )
                logger.error(f"HTTP error occurred: {http_err}")
        return self.vacancies





