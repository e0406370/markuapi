from bs4 import BeautifulSoup
from src.scrape.search.search_scraper import SearchScraper
from src.utility.endpoints import Endpoint
from src.utility.lib import Logger
from src.utility.utils import OtherInfo, PersonInfo, Utils, ViewType
from typing import Dict, List


class SearchAnimeScraper(SearchScraper):
    OTHER_INFO_FIELDS: List[OtherInfo] = [
        OtherInfo.RELEASE_DATE,
        OtherInfo.PLAYBACK_TIME,
        OtherInfo.PRODUCTION_COMPANY,
    ]

    PERSON_INFO_FIELDS: List[PersonInfo] = [
        PersonInfo.PRODUCER_1,
        PersonInfo.EXECUTIVE_PRODUCER_1,
        PersonInfo.DIRECTOR,
        PersonInfo.SERIES_COMPOSER,
        PersonInfo.CAST,
    ]

    def __init__(self, soup: BeautifulSoup, params: Dict, view: ViewType) -> None:
        super().__init__(soup, params, view)

    def set_search_results(self) -> None:
        self.search_heading = self._get_heading()

        animes = []

        if not self._is_results_empty():
            results = self._get_results_container()

            for ctr, result in enumerate(results[:int(self.results_limit)]):
                a = {}

                a["title"] = self._get_title(result)
                a["rating"] = self._get_rating(result)

                data_mark = self._get_data_mark(result)
                a["mark_count"] = data_mark.count

                data_clip = self._get_data_clip(result)
                a["clip_count"] = data_clip.count
                a["series_id"] = data_clip.anime_series_id
                a["season_id"] = data_clip.anime_season_id

                a["link"] = Utils.create_filmarks_link(Endpoint.INFO_ANIMES.value.path.format(
                    anime_series_id=data_clip.anime_series_id, 
                    anime_season_id=data_clip.anime_season_id,
                ))

                if poster := self._get_poster(result):
                    a["poster"] = poster

                for field in self.OTHER_INFO_FIELDS:
                    value = self._get_other_info(result, field)
                    if value: a[field.key] = value

                for field in self.PERSON_INFO_FIELDS:
                    value = self._get_person_info(result, field)
                    if value: a[field.key] = value

                Logger.info(self.get_logging(idx=ctr + 1, text=a))
                animes.append(a)

        self.search_results["animes"] = animes
