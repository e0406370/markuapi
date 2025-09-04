from bs4 import BeautifulSoup
from src.scrape.search.search_scraper import SearchScraper
from src.utility.endpoints import Endpoints
from src.utility.lib import Logger
from src.utility.utils import Constants, Utils
from typing import Dict, List, Tuple


class SearchMovieScraper(SearchScraper):
    OTHER_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.OTHER_INFO_SCREENING_DATE,
        Constants.OTHER_INFO_SCREENING_TIME,
        Constants.OTHER_INFO_COUNTRY_OF_ORIGIN,
        Constants.OTHER_INFO_GENRE,
        Constants.OTHER_INFO_DISTRIBUTOR,
    ]

    PERSON_INFO_FIELDS: List[Tuple[str, str]] = [
        Constants.PERSON_INFO_DIRECTOR,
        Constants.PERSON_INFO_SCRIPTWRITER,
        Constants.PERSON_INFO_CAST,
    ]

    def __init__(self, soup: BeautifulSoup, params: Dict, view: str) -> None:
        super().__init__(soup, params, view)

    def set_search_results(self) -> None:
        self.search_heading = self._get_heading()

        movies = []

        if self._is_results_empty():
            self.search_results["movies"] = movies
            return

        results = self._get_results_container()

        for ctr, result in enumerate(results[:int(self.results_limit)]):
            m = {}

            m["title"] = self._get_title(result)
            m["rating"] = self._get_rating(result)

            data_mark = self._get_data_mark(result)
            m["mark_count"] = data_mark.count

            data_clip = self._get_data_clip(result)
            m["clip_count"] = data_clip.count
            m["movie_id"] = data_clip.movie_id

            m["link"] = Utils.create_filmarks_link(Endpoints.INFO_MOVIES.value["path"].format(
                movie_id=data_clip.movie_id,
            ))

            if poster := self._get_poster(result):
                m["poster"] = poster

            for field in self.OTHER_INFO_FIELDS:
                value = self._get_other_info(result, field)
                if value: m[field[0]] = value

            for field in self.PERSON_INFO_FIELDS:
                value = self._get_person_info(result, field)
                if value: m[field[0]] = value

            Logger.info(self.get_logging(idx=ctr + 1, text=str(m)))
            movies.append(m)

        self.search_results["movies"] = movies
