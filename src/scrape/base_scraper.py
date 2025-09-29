from bs4 import BeautifulSoup
from fastapi import Request
from requests import Session
from requests.exceptions import RequestException
from src.utility.endpoints import Endpoint
from src.utility.lib import CustomException, Logger
from src.utility.utils import EndpointType, Utils, ViewType
from typing import Dict, Type, TypeVar
from urllib.parse import urlencode

T = TypeVar("T", bound="BaseScraper")


class BaseScraper:
    headers = {
        "Referer": Utils.FILMARKS_BASE,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    }

    def __init__(self, soup: BeautifulSoup, params: Dict, view: ViewType) -> None:
        self.soup = soup
        self.params = params
        self.view = view

    @classmethod
    def scrape(cls: Type[T], endpoint: Endpoint, req: Request) -> T | None:
        endpoint = endpoint.value

        if endpoint.type == EndpointType.QUERY:
            params = req.query_params
            url = Utils.create_filmarks_link(endpoint.path + "?" + urlencode(params))

        elif endpoint.type == EndpointType.PATH:
            params = req.path_params
            url = Utils.create_filmarks_link(endpoint.path.format(**params))

        elif endpoint.type == EndpointType.COMBINED:
            params = {**req.query_params, **req.path_params}
            url = Utils.create_filmarks_link(endpoint.path.format(**req.path_params) + "?" + urlencode(req.query_params))

        else:
            raise ValueError(f"Unexpected EndpointType: {endpoint.type}")  # pragma: no cover

        try:
            with Session() as session:
                resp = session.get(url=url, headers=BaseScraper.headers)
                soup = BeautifulSoup(resp.text, "lxml")

                cls._raise_if_page_service_unavailable(soup)
                cls._raise_if_page_not_found(soup)

                return cls(soup, params, endpoint.view)

        except RequestException as e:
            Logger.err(f"Request to Filmarks failed: '{e}'")
            raise CustomException.service_unavailable()

    @staticmethod
    def _raise_if_page_service_unavailable(soup: BeautifulSoup) -> None:
        status = soup.select_one("p.main__text")

        if status and status.text.strip().startswith("一時的にアクセスできない状態です。"):
            Logger.err("Filmarks is temporarily unavailable")
            raise CustomException.service_unavailable()

    @staticmethod
    def _raise_if_page_not_found(soup: BeautifulSoup) -> None:
        status = soup.select_one("p.main__status-ja")

        if status and status.text.strip() == "お探しのページは見つかりません。":
            Logger.err("Invalid Filmarks page requested")
            raise CustomException.not_found()
