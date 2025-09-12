from bs4 import BeautifulSoup
from src.scrape.info.info_scraper import InfoScraper
from src.utility.lib import Logger
from src.utility.utils import Constants
from typing import Dict, List, Tuple


class InfoMovieScraper(InfoScraper):
    OTHER_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.OTHER_INFO_SCREENING_DATE,
        Constants.OTHER_INFO_SCREENING_TIME,
        Constants.OTHER_INFO_COUNTRY_OF_ORIGIN,
        Constants.OTHER_INFO_GENRE,
        Constants.OTHER_INFO_DISTRIBUTOR,
    ]

    PERSON_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.PERSON_INFO_CREATOR,
        Constants.PERSON_INFO_DIRECTOR,
        Constants.PERSON_INFO_SCRIPTWRITER,
        Constants.PERSON_INFO_ARTIST,
        Constants.PERSON_INFO_CAST,
    ]

    def __init__(self, soup: BeautifulSoup, params: Dict, view: str) -> None:
        super().__init__(soup, params, view)

        self.movie_id = int(self.params.get("movie_id"))

    def get_logging(self) -> str:
        return f"[Movie] [ID: {self.movie_id}] {self.data}"

    def set_info_data(self) -> None:
        self.data["title"] = self._get_title()

        if original_title := self._get_original_title():
            self.data["original_title"] = original_title

        if synopsis := self._get_synopsis():
            self.data["synopsis"] = synopsis

        self.data["rating"] = self._get_rating()

        data_mark = self._get_data_mark()
        self.data["mark_count"] = data_mark.count

        data_clip = self._get_data_clip()
        self.data["clip_count"] = data_clip.count

        self.data["movie_id"] = self.movie_id
        self.data["link"] = self._get_link()

        if poster := self._get_poster():
            self.data["poster"] = poster

        if production_year := self._get_production_year():
            self.data["production_year_link"], self.data["production_year"] = production_year
        
        for field in self.OTHER_INFO_FIELDS:
            value = self._get_other_info(field)
            if value: self.data[field[0]] = value

        for field in self.PERSON_INFO_FIELDS:
            value = self._get_person_info(field)
            if value: self.data[field[0]] = value

        Logger.info(self.get_logging())
