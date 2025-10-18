from bs4 import BeautifulSoup
from src.scrape.info.info_scraper import InfoScraper
from src.utility.endpoints import Endpoint
from src.utility.lib import Logger
from src.utility.utils import OtherInfo, PersonInfo, Utils, ViewType
from typing import Dict, List


class InfoAnimeScraper(InfoScraper):
    OTHER_INFO_FIELDS: List[OtherInfo] = [
        OtherInfo.RELEASE_DATE,
        OtherInfo.PLAYBACK_TIME,
        OtherInfo.COUNTRY_OF_ORIGIN,
        OtherInfo.PRODUCTION_COMPANY,
    ]

    PERSON_INFO_FIELDS: List[PersonInfo] = [
        PersonInfo.CREATOR,
        PersonInfo.PLANNER,
        PersonInfo.PRODUCER_1,
        PersonInfo.EXECUTIVE_PRODUCER_1,
        PersonInfo.CHIEF_DIRECTOR,
        PersonInfo.DIRECTOR,
        PersonInfo.SERIES_COMPOSER,
        PersonInfo.SCRIPTWRITER,
        PersonInfo.CHARACTER_ORIGINAL_DESIGNER,
        PersonInfo.CHARACTER_DESIGNER,
        PersonInfo.NARRATOR,
        PersonInfo.ARTIST,
        PersonInfo.CAST,
    ]

    def __init__(self, soup: BeautifulSoup, params: Dict, view: ViewType) -> None:
        super().__init__(soup, params, view)

        self.series_id = int(self.params.get("anime_series_id"))
        self.season_id = int(self.params.get("anime_season_id"))
        self.review_id = int(self.params.get("review_id", -1))

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

        if official_site := self._get_official_site():
            self.data["official_site"] = official_site

        if poster := self._get_poster():
            self.data["poster"] = poster

        if production_year := self._get_production_year():
            self.data["production_year_link"], self.data["production_year"] = production_year

        for field in self.OTHER_INFO_FIELDS:
            value = self._get_other_info(field)
            if value: self.data[field.key] = value

        for field in self.PERSON_INFO_FIELDS:
            value = self._get_person_info(field)
            if value: self.data[field.key] = value

        Logger.info(self.get_logging(id=[self.series_id, self.season_id], text=self.data))

    def set_review_data(self) -> None:
        self.data["title"] = self._get_title()

        if original_title := self._get_original_title():
            self.data["original_title"] = original_title

        self.data["rating"] = self._get_rating()

        self.data["series_id"] = self.series_id
        self.data["season_id"] = self.season_id
        if self.review_id != -1:
            self.data["review_id"] = self.review_id

        self.data["link"] = Utils.create_filmarks_link(
            Endpoint.REVIEW_SPECIFIC_ANIMES.value.path.format(
                anime_series_id=self.series_id,
                anime_season_id=self.season_id,
                review_id = self.review_id
            ) 
        ) if self.review_id != -1 else self._get_link()

        if self.review_id != -1:
            self.data["review"] = self._get_review()
            Logger.info(self.get_logging(id=[self.series_id, self.season_id, self.review_id], text=self.data))

        else:
            if (condition := self._is_reviews_empty()):
                self.data["reviews"] = []
                Logger.warn(self.get_logging(id=[self.series_id, self.season_id], text=condition.text))

            else:
                self.data["reviews"] = self._get_review_info()
                Logger.info(self.get_logging(id=[self.series_id, self.season_id], text=self.data))
