from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from msgspec import Struct
from src.scrape.base_scraper import BaseScraper
from src.utility.lib import Logger, MsgSpecJSONResponse
from src.utility.utils import OtherInfo, PersonInfo, Utils, ViewType
from typing import Any, Dict, List


class SearchScraper(BaseScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict, view: ViewType) -> None:
        super().__init__(soup, params, view)

        self.results_limit = self.params.get("limit", 10)
        self.page_number = self.params.get("page", 1)

        self.search_query = self.params.get("q", "")
        self.search_heading = ""
        self.search_results = {}

    def get_response(self) -> Dict[str, Any]:
        return {
            "query": self.search_query,
            "heading": self.search_heading,
            "results": self.search_results,
            "scrape_date": Utils.get_scrape_date(),
        }

    def get_logging(self, idx: int, text: str) -> str:
        return f"[{self.view.value}] [{idx} | Query: {self.search_query} | Heading: {self.search_heading} | Page: {self.page_number}] {text}"

    def _get_heading(self) -> str:
        selectors = ["h1.c-heading-1", "h1.c-page-title__title"]
        for sel in selectors:
            if heading := self.soup.select_one(sel):
                return heading.text

        return ""

    def _is_results_empty(self) -> Tag | None:
        condition = self.soup.select_one("div.p-timeline__zero")
        if condition:
            Logger.warn(self.get_logging(idx=0, text=condition.text))

        return condition

    def _get_results_container(self) -> ResultSet[Tag]:
        container = self.soup.select("div.p-contents-grid > div.js-cassette")

        return container

    def _get_title(self, result: Tag) -> str:
        return result.select_one("h3.p-content-cassette__title").text

    def _get_rating(self, result: Tag) -> float | str:
        rating = result.select_one("div.c-rating__score").text

        return float(rating) if rating != "-" else rating

    def _get_data_mark(self, result: Tag) -> Struct:
        return MsgSpecJSONResponse.parse(content=result.attrs["data-mark"], type=self.view.mark)

    def _get_data_clip(self, result: Tag) -> Struct:
        return MsgSpecJSONResponse.parse(content=result.attrs["data-clip"], type=self.view.clip)

    def _get_poster(self, result: Tag) -> str | None:
        poster = result.select_one("div.c2-poster-m > img")

        return poster.attrs["src"] if poster else None

    def _get_other_info(self, result: Tag, field: OtherInfo) -> str | List[str] | None:
        if field == OtherInfo.GENRE:
            info_elem = result.find("h4", class_="p-content-cassette__genre-title")

        elif field == OtherInfo.DISTRIBUTOR:
            info_elem = result.find("h4", class_="p-content-cassette__distributor-title")

        else:
            info_elem = result.find("h4", class_="p-content-cassette__other-info-title", string=field.title)

        if field in OtherInfo.single_fields():
            return info_elem.find_next_sibling("span").text if info_elem else None

        else:
            return [name.text for name in info_elem.find_next_sibling("ul").find_all("a")] if info_elem else None

    def _get_person_info(self, result: Tag, field: PersonInfo) -> List[str] | None:
        info_elem = result.find("h4", class_="p-content-cassette__people-list-term", string=field.title)
        
        return [name.text for name in info_elem.find_next_sibling("ul").find_all("a")] if info_elem else None
