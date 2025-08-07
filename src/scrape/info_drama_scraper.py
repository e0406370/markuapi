from bs4 import BeautifulSoup
from datetime import datetime, timezone
from src.scrape.base_scraper import BaseScraper
from src.utility.lib import Logger, MsgSpecJSONResponse
from src.utility.models import DataClip, DataMark, Filmarks
from typing import Any, List, Dict, Tuple


class InfoDramaScraper(BaseScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict) -> None:
        super().__init__(soup, params)

        self.series_id = int(self.params.get("drama_series_id"))
        self.season_id = int(self.params.get("drama_season_id"))

        self.data = {}

    def get_response(self) -> Dict[str, Any]:
        return {
            "series_id": self.series_id,
            "season_id": self.season_id,
            "data": self.data,
            "scrape_date": datetime.now(timezone.utc).isoformat(),
        }

    def _get_title(self) -> str:
        return self.soup.select_one("h2.p-content-detail__title > span").text

    def _get_original_title(self) -> str | None:
        title_elem = self.soup.select_one("p.p-content-detail__original")

        return title_elem.text if title_elem else None

    def _get_rating(self) -> float:
        rating = self.soup.select_one("div.c2-rating-l__text").text

        return float(rating) if rating != "-" else rating

    def _get_data_mark(self) -> DataMark:
        data_elem = self.soup.select_one("div.c-content__counts > div.js-btn-mark")

        return MsgSpecJSONResponse.parse(content=data_elem.attrs["data-mark"], type=DataMark)

    def _get_data_clip(self) -> DataClip:
        data_elem = self.soup.select_one("div.c-content__counts > div.js-btn-clip")

        return MsgSpecJSONResponse.parse(content=data_elem.attrs["data-clip"], type=DataClip)

    def _get_link(self) -> str:
        return self.soup.select_one("link").attrs["href"]

    def _get_poster(self) -> str | None:
        poster_elem = self.soup.select_one("div.c2-poster-l > img")

        return poster_elem.attrs["src"] if poster_elem else None
    
    def _get_production_year(self) -> Tuple[str]:
        title_elem = self.soup.select_one("h2.p-content-detail__title a")

        return Filmarks.create_filmarks_link(title_elem.attrs["href"]), title_elem.text

    def _get_other_info(self, type: str) -> str | None: 
        match type:
            case "release_date":
                string_filter = "公開日："

            case "country_of_origin":
                string_filter = "製作国："

            case "playback_time":
                string_filter = "再生時間："

            case _:
                raise ValueError("type can only be 'release_date', 'country_of_origin', or 'playback_time'!")

        title_elem = self.soup.find("h3", class_="p-content-detail__other-info-title", string=lambda s: s and s.startswith(string_filter))

        match type:
            case "release_date" | "playback_time":
                return title_elem.text.split(string_filter)[1] if title_elem else None

            case "country_of_origin":
                return title_elem.find_next("a").text if title_elem else None

    def _get_synopsis(self) -> str | None:
        title_elem = self.soup.select_one("#js-content-detail-synopsis")

        return title_elem.select_one("content-detail-synopsis").get(":outline").strip('"') if title_elem else None

    def _get_genre(self) -> List[str] | None:
        title_elem = self.soup.select_one("h3.p-content-detail__genre-title")

        return [genre.text for genre in title_elem.find_next_sibling("ul").find_all("a")] if title_elem else None

    def _get_people_list(self, type: str) -> List[Dict[str, Any]] | None:
        match type:
            case "creator":
                title_elem = self.soup.find("h3", class_="p-content-detail__people-list-term", string="原作")

            case "director":
                title_elem = self.soup.find("h3", class_="p-content-detail__people-list-term", string="監督")

            case "scriptwriter":
                title_elem = self.soup.find("h3", class_="p-content-detail__people-list-term", string="脚本")

            case "artist":
                title_elem = self.soup.find("h3", class_="p-content-detail__people-list-term", string="主題歌／挿入歌")

            case _:
                raise ValueError("type can only be 'creator', 'director', 'scriptwriter', or 'artist'!")

        return [
            Filmarks.create_person_info(
                name=person.find("div").text, 
                link=person.find("a").attrs["href"]
            )
            for person
            in title_elem.find_next_sibling("ul").find_all("li")
        ] if title_elem else None

    def _get_cast(self) -> List[Dict[str, Any]] | None:
        title_elem = self.soup.select_one("div.p-people-list__casts")

        return [
            Filmarks.create_person_info(
                name=cast.select_one("div.c2-button-tertiary-s-multi-text__text").text,
                link=cast.select_one("a").attrs["href"],
                character=character.text if (character := cast.select_one("div.c2-button-tertiary-s-multi-text__subtext")) else ""
            )
            for cast
            in title_elem.select("h4.p-people-list__item")
        ] if title_elem else None

    def set_info_data(self) -> None:
        self._raise_if_page_not_found()

        self.data["title"] = self._get_title()

        if original_title := self._get_original_title():
            self.data["original_title"] = original_title

        self.data["rating"] = self._get_rating()

        data_mark = self._get_data_mark()
        self.data["mark_count"] = data_mark.count

        data_clip = self._get_data_clip()
        self.data["clip_count"] = data_clip.count

        self.data["link"] = self._get_link()

        if poster := self._get_poster():
            self.data["poster"] = poster

        self.data["production_year_series"], self.data["production_year"] = self._get_production_year()

        if release_date := self._get_other_info("release_date"):
            self.data["release_date"] = release_date  

        if country_of_origin := self._get_other_info("country_of_origin"):
            self.data["country_of_origin"] = country_of_origin

        if playback_time := self._get_other_info("playback_time"):
            self.data["playback_time"] = playback_time
            
        if synopsis := self._get_synopsis():
            self.data["synopsis"] = synopsis

        if genre := self._get_genre():
            self.data["genre"] = genre

        if creator := self._get_people_list("creator"):
            self.data["creator"] = creator

        if director := self._get_people_list("director"):
            self.data["director"] = director

        if scriptwriter := self._get_people_list("scriptwriter"):
            self.data["scriptwriter"] = scriptwriter

        if artist := self._get_people_list("artist"):
            self.data["artist"] = artist

        if cast := self._get_cast():
            self.data["cast"] = cast

        Logger.info(f"[Series ID: {self.series_id}, Season ID: {self.season_id}] {str(self.data)}")