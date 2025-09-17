from bs4 import BeautifulSoup
from bs4.element import Tag
from msgspec import Struct
from src.scrape.base_scraper import BaseScraper
from src.utility.lib import MsgSpecJSONResponse
from src.utility.utils import Constants, Utils
from typing import Any, Dict, List, Tuple


class InfoScraper(BaseScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict, view: str) -> None:
        super().__init__(soup, params, view)

        self.detail_head = self.soup.select_one("div.p-content-detail__head")
        self.detail_foot = self.soup.select_one("div.p-content-detail__foot")

        self.page_number = int(self.params.get("page", 1))
        self.data = {}

    def get_response(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "scrape_date": Utils.get_scrape_date(),
        }

    def get_logging(self, id: List[int], text: str) -> str:
        return f"[{self.view}] [ID: {', '.join(str(i) for i in id)}] {text}"

    def _get_title(self) -> str:
        selectors = ["h2.p-content-detail__title > span", "h2.c-content-box-s__title"]
        for sel in selectors:
            if title := self.detail_head.select_one(sel):
                return title.text

    def _get_original_title(self) -> str | None:
        selectors = ["p.p-content-detail__original", "p.c-content-box-s__original"]
        for sel in selectors:
            if title := self.detail_head.select_one(sel):
                return title.text

        return None

    def _get_synopsis(self) -> str | None:
        synopsis = self.detail_head.select_one("#js-content-detail-synopsis")

        return synopsis.select_one("content-detail-synopsis").get(":outline").strip('"') if synopsis else None

    def _get_rating(self) -> float | str:
        selectors = ["div.c2-rating-l__text", "div.c2-rating-m__text"]
        for sel in selectors:
            if rating := self.detail_head.select_one(sel):
                rating = rating.text
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

    def _get_production_year(self) -> Tuple[str] | None:
        production_year = self.detail_head.select_one("h2.p-content-detail__title a")

        return (Utils.create_filmarks_link(production_year.attrs["href"]), int(production_year.text.replace("年", ""))) if production_year else None

    def _get_other_info(self, field: Tuple[str, str]) -> str | List[Dict[str, Any]] | None:
        if field not in Constants.OTHER_INFO:
            Utils.raise_value_error("field", Constants.OTHER_INFO)

        if field == Constants.OTHER_INFO_GENRE:
            info_elem = self.detail_head.select_one("h3.p-content-detail__genre-title")

        else:
            info_elem = self.detail_head.find("h3", class_="p-content-detail__other-info-title", string=lambda s: s.startswith(field[1]))

        if field in Constants.OTHER_INFO_SINGLE:
            return info_elem.text.replace(field[1], "") if info_elem else None

        elif self.view == Constants.VIEW_ANIME and field == Constants.OTHER_INFO_COUNTRY_OF_ORIGIN:
            return [name.text for name in info_elem.find_next_sibling("ul").find_all("li")] if info_elem else None

        else:
            return [
                Utils.create_other_info(
                    name=other.text,
                    link=other.attrs["href"]
                )
                for other
                in info_elem.find_next_sibling("ul").find_all("a")
            ] if info_elem else None

    def _get_person_info(self, field: Tuple[str, str]) -> List[Dict[str, Any]] | None:
        if field not in Constants.PERSON_INFO:
            Utils.raise_value_error("field", Constants.PERSON_INFO)

        if field == Constants.PERSON_INFO_CAST:
            info_elem = self.detail_head.select_one("div.p-people-list__casts")

            return [
                Utils.create_person_info(
                    name=person.select_one("div.c2-button-tertiary-s-multi-text__text").text,
                    link=person.select_one("a").attrs["href"],
                    character=character.text if (character := person.select_one("div.c2-button-tertiary-s-multi-text__subtext")) else ""
                )
                for person
                in info_elem.select("h4.p-people-list__item")
            ] if info_elem else None

        else:
            info_elem = self.detail_head.find("h3", class_="p-content-detail__people-list-term", string=field[1])

            return [
                Utils.create_person_info(
                    name=person.find("div").text, 
                    link=person.find("a").attrs["href"]
                )
                for person
                in info_elem.find_next_sibling("ul").find_all("li")
            ] if info_elem else None

    def _is_reviews_empty(self) -> Tag | None:
        condition = self.detail_foot.select_one("div.p2-empty-reviews-message__text")

        return condition

    def _get_review_info(self) -> List[Dict[str, Any]] | None:
        info_elem = self.detail_foot.select("div.p-mark")

        return [
            Utils.create_review_info(
                user_name=review.select_one("div.c2-user-m__heading a").text.replace("の感想・評価", ""),
                user_link=review.select_one("div.c2-user-m > a").attrs["href"],
                review_date=review.select_one("time.c-media__date").text,
                review_rating=float(rating) if (rating := review.select_one("div.c2-rating-s__text").text) != "-" else rating,
                review_link=review.select_one("div.c2-user-m__heading a").attrs["href"],
                review_contents= rev.get_text(separator=" ", strip=True) if (rev := review.select_one("div.p-mark-review")) else ""
            )
            for review
            in info_elem
        ] if info_elem else None
