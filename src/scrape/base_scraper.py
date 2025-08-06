from bs4 import BeautifulSoup
from src.utility.lib import CustomException, Logger
from src.utility.models import Filmarks
from typing import Dict, Type, TypeVar
from urllib.parse import urlencode
import requests

T = TypeVar("T", bound="BaseScraper")


class BaseScraper:
    def __init__(self, soup: BeautifulSoup, params: Dict) -> None:
        self.soup = soup
        self.params = params

    @classmethod
    def scrape(cls: Type[T], endpoint: str, params: Dict) -> T | None:
        if endpoint in Filmarks.SEARCH_ENDPOINTS:
            url = Filmarks.create_filmarks_link(endpoint + "?" + urlencode(params))

        elif endpoint in Filmarks.INFO_ENDPOINTS:
            url = Filmarks.create_filmarks_link(endpoint.format(**params))

        else:
            Logger.err(f"Invalid endpoint requested: '{endpoint}'")

            raise CustomException.not_found()

        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "lxml")

            return cls(soup, params)

        except requests.exceptions.RequestException as e:
            Logger.err(f"Request to Filmarks failed: '{e}'")

            raise CustomException.service_unavailable()

    def _raise_if_page_not_found(self) -> None:
        status = self.soup.select_one("p.main__status-ja")

        if status and status.text.strip() == "お探しのページは見つかりません。":
            Logger.err("Invalid Filmarks page requested")

            raise CustomException.not_found()
