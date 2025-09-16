from bs4 import BeautifulSoup
from src.scrape.search.search_scraper import SearchScraper
from src.utility.endpoints import Endpoints
from src.utility.lib import Logger
from src.utility.utils import Constants, Utils
from typing import Dict, List, Tuple


class SearchDramaScraper(SearchScraper):
    OTHER_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.OTHER_INFO_RELEASE_DATE,
        Constants.OTHER_INFO_PLAYBACK_TIME,
        Constants.OTHER_INFO_COUNTRY_OF_ORIGIN,
        Constants.OTHER_INFO_GENRE,
    ]

    PERSON_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.PERSON_INFO_EXECUTIVE_PRODUCER_2,
        Constants.PERSON_INFO_DIRECTOR,
        Constants.PERSON_INFO_SCRIPTWRITER,
        Constants.PERSON_INFO_CAST,
    ]

    def __init__(self, soup: BeautifulSoup, params: Dict, view: str) -> None:
        super().__init__(soup, params, view)

    def set_search_results(self) -> None:
        self.search_heading = self._get_heading()

        dramas = []

        if not self._is_results_empty():
            results = self._get_results_container()

            for ctr, result in enumerate(results[:int(self.results_limit)]):
                d = {}

                d["title"] = self._get_title(result)
                d["rating"] = self._get_rating(result)

                data_mark = self._get_data_mark(result)
                d["mark_count"] = data_mark.count

                data_clip = self._get_data_clip(result)
                d["clip_count"] = data_clip.count
                d["series_id"] = data_clip.drama_series_id
                d["season_id"] = data_clip.drama_season_id

                d["link"] = Utils.create_filmarks_link(Endpoints.INFO_DRAMAS.value["path"].format(
                    drama_series_id=data_clip.drama_series_id, 
                    drama_season_id=data_clip.drama_season_id,
                ))

                if poster := self._get_poster(result):
                    d["poster"] = poster

                for field in self.OTHER_INFO_FIELDS:
                    value = self._get_other_info(result, field)
                    if value: d[field[0]] = value

                for field in self.PERSON_INFO_FIELDS:
                    value = self._get_person_info(result, field)
                    if value: d[field[0]] = value

                Logger.info(self.get_logging(idx=ctr + 1, text=d))
                dramas.append(d)

        self.search_results["dramas"] = dramas
