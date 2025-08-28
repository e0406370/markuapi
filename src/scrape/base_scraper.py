from bs4 import BeautifulSoup
from fastapi import Request
from src.utility.lib import CustomException, Logger
from src.utility.models import Filmarks
from typing import Dict, Type, TypeVar
from urllib.parse import urlencode
import requests

T = TypeVar("T", bound="BaseScraper")


class BaseScraper:
    headers = {
        "Referer": Filmarks.FILMARKS_BASE,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",        
    }

    def __init__(self, soup: BeautifulSoup, params: Dict) -> None:
        self.soup = soup
        self.params = params

    @classmethod
    def scrape(cls: Type[T], endpoint: Dict[str, str], req: Request) -> T | None:
        cls._raise_if_invalid_endpoint(endpoint)

        if endpoint["type"] == "query":
            params = req.query_params
            url = Filmarks.create_filmarks_link(endpoint["path"] + "?" + urlencode(params))

        elif endpoint["type"] == "path":
            params = req.path_params
            url = Filmarks.create_filmarks_link(endpoint["path"].format(**params))

        elif endpoint["type"] == "path+query":
            params = {**req.query_params, **req.path_params}
            url = Filmarks.create_filmarks_link(endpoint["path"].format(**req.path_params) + "?" + urlencode(req.query_params))

        else:
            raise ValueError("type can only be 'path', 'query', or 'path+query'!")

        try:
            with requests.Session() as session:
                resp = session.get(url=url, headers=BaseScraper.headers)
                soup = BeautifulSoup(resp.text, "lxml")

                cls._raise_if_page_not_found(soup)

                return cls(soup, params)

        except requests.exceptions.RequestException as e:
            Logger.err(f"Request to Filmarks failed: '{e}'")

            raise CustomException.service_unavailable()

    @staticmethod
    def _raise_if_invalid_endpoint(endpoint: Dict[str, str]) -> None:
        if endpoint not in Filmarks.Endpoints:
            Logger.err(f"Invalid endpoint requested: '{endpoint}'")

            raise CustomException.not_found()

    @staticmethod
    def _raise_if_page_not_found(soup: BeautifulSoup) -> None:
        status = soup.select_one("p.main__status-ja")

        if status and status.text.strip() == "お探しのページは見つかりません。":
            Logger.err("Invalid Filmarks page requested")

            raise CustomException.not_found()
