from bs4 import BeautifulSoup
from msgspec import Struct
from src.scrape.base_scraper import BaseScraper
from src.utility.lib import MsgSpecJSONResponse
from src.utility.utils import Constants, Utils
from typing import Any, Dict, List, Tuple


class InfoScraper(BaseScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict, view: str) -> None:
        super().__init__(soup, params, view)
        
        self.detail_head = self.soup.select_one("div.p-content-detail__head")
        self.data = {}

    def get_response(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "scrape_date": Utils.get_scrape_date(),
        }

    def _get_title(self) -> str:
        return self.detail_head.select_one("h2.p-content-detail__title > span").text

    def _get_original_title(self) -> str | None:
        title_elem = self.detail_head.select_one("p.p-content-detail__original")

        return title_elem.text if title_elem else None

    def _get_synopsis(self) -> str | None:
        title_elem = self.detail_head.select_one("#js-content-detail-synopsis")

        return title_elem.select_one("content-detail-synopsis").get(":outline").strip('"') if title_elem else None

    def _get_rating(self) -> float | str:
        rating = self.detail_head.select_one("div.c2-rating-l__text").text

        return float(rating) if rating != "-" else rating

    def _get_data_mark(self) -> Struct:
        if self.view not in Constants.MARKS:
            Utils.raise_value_error("view", Constants.VIEWS)

        selectors = ["div.c-content__counts > div.js-btn-mark", "div.c-content__actions > div.js-btn-mark"]
        for sel in selectors:
            if data_elem := self.detail_head.select_one(sel):
                return MsgSpecJSONResponse.parse(content=data_elem.attrs["data-mark"], type=Constants.MARKS[self.view])

    def _get_data_clip(self) -> Struct:
        if self.view not in Constants.CLIPS:
            Utils.raise_value_error("view", Constants.VIEWS)

        selectors = ["div.c-content__counts > div.js-btn-clip", "div.c-content__actions > div.js-btn-clip"]
        for sel in selectors:
            if data_elem := self.detail_head.select_one(sel):
                return MsgSpecJSONResponse.parse(content=data_elem.attrs["data-clip"], type=Constants.CLIPS[self.view])

    def _get_link(self) -> str:
        return self.soup.select_one("link").attrs["href"]

    def _get_poster(self) -> str | None:
        poster = self.detail_head.select_one("div.c2-poster-l > img")

        return poster.attrs["src"] if poster else None

    def _get_production_year(self) -> Tuple[str]:
        title_elem = self.detail_head.select_one("h2.p-content-detail__title a")

        return Utils.create_filmarks_link(title_elem.attrs["href"]), title_elem.text

    def _get_other_info(self, field: Tuple[str, str]) -> str | List[Dict[str, Any]] | None:
        if field not in Constants.OTHER_INFO:
            Utils.raise_value_error("field", Constants.OTHER_INFO)

        if field == Constants.OTHER_INFO_GENRE:
            title_elem = self.detail_head.select_one("h3.p-content-detail__genre-title")

        else:
            title_elem = self.detail_head.find("h3", class_="p-content-detail__other-info-title", string=lambda s: s and s.startswith(field[1]))

        if field in Constants.OTHER_INFO_SINGLE:
            return title_elem.text.split(field[1])[1] if title_elem else None
        
        elif self.view == Constants.VIEW_ANIME and field == Constants.OTHER_INFO_COUNTRY_OF_ORIGIN:
            return title_elem.find_next_sibling("ul").find("li").text if title_elem else None

        else:
            return [
                Utils.create_other_info(
                    name=other.text,
                    link=other.attrs["href"]
                )
                for other
                in title_elem.find_next_sibling("ul").find_all("a")
            ] if title_elem else None

    def _get_person_info(self, field: Tuple[str, str]) -> List[Dict[str, Any]] | None:
        if field not in Constants.PERSON_INFO:
            Utils.raise_value_error("field", Constants.PERSON_INFO)

        if field == Constants.PERSON_INFO_CAST:
            title_elem = self.detail_head.select_one("div.p-people-list__casts")
            
            return [
                Utils.create_person_info(
                    name=person.select_one("div.c2-button-tertiary-s-multi-text__text").text,
                    link=person.select_one("a").attrs["href"],
                    character=character.text if (character := person.select_one("div.c2-button-tertiary-s-multi-text__subtext")) else ""
                )
                for person
                in title_elem.select("h4.p-people-list__item")
            ] if title_elem else None
            
        else:
            title_elem = self.detail_head.find("h3", class_="p-content-detail__people-list-term", string=field[1])
            
            return [
                Utils.create_person_info(
                    name=person.find("div").text, 
                    link=person.find("a").attrs["href"]
                )
                for person
                in title_elem.find_next_sibling("ul").find_all("li")
            ] if title_elem else None
