from bs4 import BeautifulSoup
from fastapi import HTTPException, status
from src.utility.lib import Logger
from src.utility.models import Filmarks
from urllib.parse import urlencode, urljoin
from typing import Type, TypeVar
import requests

T = TypeVar("T", bound="BaseScraper")


class BaseScraper:
    def __init__(self, soup: BeautifulSoup, params: dict) -> None:
        self.soup = soup
        self.params = params

    @classmethod
    def scrape(cls: Type[T], endpoint: str, params: dict) -> T | None:
        if endpoint in Filmarks.SEARCH_ENDPOINTS:
            url = urljoin(base=Filmarks.FILMARKS_BASE, url=endpoint + "?" + urlencode(params))

        elif endpoint in Filmarks.INFO_ENDPOINTS:
            url = urljoin(base=Filmarks.FILMARKS_BASE, url=endpoint.format(**params))

        else:
            Logger.err(f"Invalid endpoint requested: '{endpoint}'")

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The requested resource could not be found.",
            )

        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "lxml")

            return cls(soup, params)

        except requests.exceptions.RequestException as e:
            Logger.err(f"Request to Filmarks failed: '{e}'")

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="The service is currently unavailable.",
            )
