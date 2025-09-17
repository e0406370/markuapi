from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from jsonpath_ng import parse
from requests import get
from src.api import api
from src.scrape.base_scraper import BaseScraper
from src.utility.utils import Constants
from typing import Any, Optional

client = TestClient(api)


def get_json_val(json: Any, path: str) -> Optional[Any]:
    query = parse(path)
    match = query.find(json)
    return match[0].value if match else None


def get_reviews_last_page(slug: str) -> int:
    resp = get(url=f"{Constants.FILMARKS_BASE}{slug}", headers=BaseScraper.headers)
    soup = BeautifulSoup(resp.text, "lxml")

    last = soup.select_one("div.p-timeline a.c2-pagination__last")
    return 1 if not last else int(last.attrs["href"].split("?page=")[-1])
