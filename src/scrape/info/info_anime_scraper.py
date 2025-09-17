from bs4 import BeautifulSoup
from src.scrape.info.info_scraper import InfoScraper
from src.utility.lib import Logger
from src.utility.utils import Constants
from typing import Dict, List, Tuple


class InfoAnimeScraper(InfoScraper):
    OTHER_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.OTHER_INFO_RELEASE_DATE,
        Constants.OTHER_INFO_PLAYBACK_TIME,
        Constants.OTHER_INFO_COUNTRY_OF_ORIGIN,
        Constants.OTHER_INFO_PRODUCTION_COMPANY,
    ]

    PERSON_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.PERSON_INFO_CREATOR,
        Constants.PERSON_INFO_PLANNER,
        Constants.PERSON_INFO_PRODUCER_1,
        Constants.PERSON_INFO_EXECUTIVE_PRODUCER_1,
        Constants.PERSON_INFO_CHIEF_DIRECTOR,
        Constants.PERSON_INFO_DIRECTOR,
        Constants.PERSON_INFO_SERIES_COMPOSER,
        Constants.PERSON_INFO_SCRIPTWRITER,
        Constants.PERSON_INFO_CHARACTER_ORIGINAL_DESIGNER,
        Constants.PERSON_INFO_CHARACTER_DESIGNER,
        Constants.PERSON_INFO_NARRATOR,
        Constants.PERSON_INFO_ARTIST,
        Constants.PERSON_INFO_CAST,
    ]

    def __init__(self, soup: BeautifulSoup, params: Dict, view: str) -> None:
        super().__init__(soup, params, view)

        self.series_id = int(self.params.get("anime_series_id"))
        self.season_id = int(self.params.get("anime_season_id"))

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

        self.data["series_id"] = self.series_id
        self.data["season_id"] = self.season_id
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

        Logger.info(self.get_logging(id=[self.series_id, self.season_id], text=self.data))

    def set_review_data(self) -> None:
        self.data["title"] = self._get_title()

        if original_title := self._get_original_title():
            self.data["original_title"] = original_title

        self.data["rating"] = self._get_rating()

        self.data["series_id"] = self.series_id
        self.data["season_id"] = self.season_id
        self.data["link"] = self._get_link()
        
        self.data["page"] = self.page_number

        if (condition := self._is_reviews_empty()):
            self.data["reviews"] = []
            Logger.warn(self.get_logging(id=[self.series_id, self.season_id], text=condition.text))

        else:
            self.data["reviews"] = self._get_review_info()
            Logger.info(self.get_logging(id=[self.series_id, self.season_id], text=self.data))
