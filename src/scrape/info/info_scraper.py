from bs4 import BeautifulSoup
from bs4.element import Tag
from msgspec import Struct
from src.scrape.base_scraper import BaseScraper
from src.utility.lib import MsgSpecJSONResponse
from src.utility.utils import OtherInfo, PersonInfo, Utils, ViewType
from typing import Any, Dict, List, Tuple


class InfoScraper(BaseScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict, view: ViewType) -> None:
        super().__init__(soup, params, view)

        self.detail_head = self.soup.select_one("div.p-content-detail__head") or self.soup.select_one("div.p-timeline-mark")
        self.detail_foot = self.soup.select_one("div.p-content-detail__foot") or self.soup.select_one("div.p-profile__main")

        self.page_number = int(self.params.get("page", 1))
        self.data = {}

    def get_response(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "scrape_date": Utils.get_scrape_date(),
        }

    def get_logging(self, id: List[int], text: str) -> str:
        return f"[{self.view.value}] [ID: {', '.join(str(i) for i in id)}] {text}"

    def _get_title(self) -> str:
        selectors = ["h2.p-content-detail__title > span", "h2.c-content-box-s__title", "div.p-timeline-mark__title > a"]
        for sel in selectors:
            if title := self.detail_head.select_one(sel):
                return title.find(string=True, recursive=False).text

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
        selectors = ["div.c2-rating-l__text", "div.c2-rating-m__text", "div.c-rating__score"]
        for sel in selectors:
            if rating := self.detail_head.select_one(sel):
                rating = rating.text
                return float(rating) if rating != "-" else rating

    def _get_data_mark(self) -> Struct:
        selectors = ["div.c-content__counts > div.js-btn-mark", "div.c-content__actions > div.js-btn-mark"]
        for sel in selectors:
            if data_elem := self.detail_head.select_one(sel):
                return MsgSpecJSONResponse.parse(content=data_elem.attrs["data-mark"], type=self.view.mark)

    def _get_data_clip(self) -> Struct:
        selectors = ["div.c-content__counts > div.js-btn-clip", "div.c-content__actions > div.js-btn-clip"]
        for sel in selectors:
            if data_elem := self.detail_head.select_one(sel):
                return MsgSpecJSONResponse.parse(content=data_elem.attrs["data-clip"], type=self.view.clip)

    def _get_link(self) -> str:
        return self.soup.select_one("link").attrs["href"]

    def _get_official_site(self) -> str | None:
        link = self.detail_head.select_one("li.p-content-detail-links__item--official > a")

        return link.attrs["href"] if link else None

    def _get_poster(self) -> str | None:
        poster = self.detail_head.select_one("div.c2-poster-l > img")

        return poster.attrs["src"] if poster else None

    def _get_production_year(self) -> Tuple[str] | None:
        production_year = self.detail_head.select_one("h2.p-content-detail__title a")

        return (Utils.create_filmarks_link(production_year.attrs["href"]), int(production_year.text.replace("年", ""))) if production_year else None

    def _get_other_info(self, field: OtherInfo) -> str | List[str] | List[Dict[str, Any]] | None:
        if field == OtherInfo.GENRE or field == OtherInfo.DISTRIBUTOR:
            info_elem = self.detail_head.find("h3", class_="p-content-detail__secondary-info-title", string=lambda s: s.startswith(field.title))

        else:
            info_elem = self.detail_head.find("h3", class_="p-content-detail__primary-info-title", string=lambda s: s.startswith(field.title))

        if field in OtherInfo.single_fields():
            return info_elem.text.replace(field.title, "") if info_elem else None

        elif self.view == ViewType.ANIME and field == OtherInfo.COUNTRY_OF_ORIGIN:
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

    def _get_person_info(self, field: PersonInfo) -> List[Dict[str, Any]] | None:
        if field == PersonInfo.CAST:
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
            info_elem = self.detail_head.find("h3", class_="p-content-detail__people-list-term", string=field.title)

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
    
    def _get_review(self) -> Dict[str, Any]:
        return Utils.create_review_info(
            user_name=self.detail_foot.select_one("h2.p-profile__name > a").text,
            user_link=self.detail_foot.select_one("div.p-profile__content > a").attrs["href"],
            review_date=self.detail_head.select_one("time.c-media__date").text,
            review_rating=float(rating) if (rating := self.detail_head.select_one("div.c-rating__score").text) != "-" else rating,
            review_contents=self.detail_head.select_one("div.p-mark-review").get_text(separator=" ", strip=True),
        )

    def _get_review_info(self) -> List[Dict[str, Any]] | None:
        info_elem = self.detail_foot.select("div.p-mark")

        return [
            Utils.create_review_info(
                user_name=review.select_one("div.c2-user-m__heading a").text.replace("の感想・評価", ""),
                user_link=review.select_one("div.c2-user-m > a").attrs["href"],
                review_date=review.select_one("time.c-media__date").text,
                review_rating=float(rating) if (rating := review.select_one("div.c2-rating-s__text").text) != "-" else rating,
                review_contents= rev.get_text(separator=" ", strip=True) if (rev := review.select_one("div.p-mark-review")) else "",
                review_link=review.select_one("div.c2-user-m__heading a").attrs["href"],
            )
            for review
            in info_elem
        ] if info_elem else None
