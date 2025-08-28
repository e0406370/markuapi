from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from datetime import datetime, timezone
from src.scrape.base_scraper import BaseScraper
from src.utility.lib import Logger
from typing import Any, Dict


class SearchScraper(BaseScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict) -> None:
        super().__init__(soup, params)

        self.results_limit = self.params.get("limit", 10)
        self.page_number = self.params.get("page", 1)
        self.search_query = self.params.get("q", "")

        self.search_results = {}
        self.search_heading = ""

    def get_response(self) -> Dict[str, Any]:
        return {
            "query": self.search_query,
            "results": self.search_results,
            "heading": self.search_heading,
            "scrape_date": datetime.now(timezone.utc).isoformat(sep=" ", timespec="seconds"),
        }

    def get_logging_result(self, idx: int, text: str) -> str:
        return f"[{idx} | Query: {self.search_query} | Page: {self.page_number}] {text}"

    def _is_results_empty(self) -> bool:
        condition = self.soup.select_one("div.p-timeline__zero")
        if condition: Logger.warn(self.get_logging_result(idx=0, text="一致する情報は見つかりませんでした。"))

        return condition

    def _get_results_container(self) -> ResultSet[Tag]:
        container = self.soup.select_one(
          "div.p-contents-grid"
        ).select(
          "div.js-cassette"
        )

        return container

    def _get_heading(self) -> str:
        return self.soup.select_one("h1.c-heading-1").text
