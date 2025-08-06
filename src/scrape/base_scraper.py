from bs4 import BeautifulSoup
from src.utility.lib import CustomException, Logger
from src.utility.models import Filmarks
from urllib.parse import urlencode, urljoin
from typing import Dict, Type, TypeVar
import requests

T = TypeVar("T", bound="BaseScraper")


class BaseScraper:
    def __init__(self, soup: BeautifulSoup, params: Dict) -> None:
        self.soup = soup
        self.params = params

    @classmethod
    def scrape(cls: Type[T], endpoint: str, params: Dict) -> T | None:
        if endpoint in Filmarks.SEARCH_ENDPOINTS:
            url = urljoin(base=Filmarks.FILMARKS_BASE, url=endpoint + "?" + urlencode(params))

        elif endpoint in Filmarks.INFO_ENDPOINTS:
            url = urljoin(base=Filmarks.FILMARKS_BASE, url=endpoint.format(**params))

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
