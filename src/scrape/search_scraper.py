from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.scrape.base_scraper import BaseScraper
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
            "scrape_date": datetime.now(timezone.utc).isoformat(),
            "heading": self.search_heading,
        }
