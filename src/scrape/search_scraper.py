from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.scrape.base_scraper import BaseScraper
from typing import Any, Dict


class SearchScraper(BaseScraper):
    def __init__(self, soup: BeautifulSoup, params: dict) -> None:
        super().__init__(soup, params)

        self.search_query = self.params.get("q", "")
        self.search_results = {}

    def get_response(self) -> Dict[str, Any]:
        return {
            "query": self.search_query,
            "results": self.search_results,
            "scrape_date": datetime.now(timezone.utc).isoformat(),
        }
