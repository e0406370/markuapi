from bs4 import BeautifulSoup
from src.scrape.search.search_scraper import SearchScraper
from src.utility.endpoints import Endpoint
from src.utility.lib import Logger
from src.utility.utils import OtherInfo, PersonInfo, Utils, ViewType
from typing import Dict, List


class SearchMovieScraper(SearchScraper):
    OTHER_INFO_FIELDS: List[OtherInfo] = [
        OtherInfo.SCREENING_DATE,
        OtherInfo.SCREENING_TIME,
        OtherInfo.COUNTRY_OF_ORIGIN,
        OtherInfo.GENRE,
        OtherInfo.DISTRIBUTOR,
    ]

    PERSON_INFO_FIELDS: List[PersonInfo] = [
        PersonInfo.DIRECTOR,
        PersonInfo.SCRIPTWRITER,
        PersonInfo.CAST,
    ]

    def __init__(self, soup: BeautifulSoup, params: Dict, view: ViewType) -> None:
        super().__init__(soup, params, view)

    def set_search_results(self) -> None:
        self.search_heading = self._get_heading()

        movies = []

        if not self._is_results_empty():
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

                m["link"] = Utils.create_filmarks_link(Endpoint.INFO_MOVIES.value.path.format(
                    movie_id=data_clip.movie_id,
                ))

                if poster := self._get_poster(result):
                    m["poster"] = poster

                for field in self.OTHER_INFO_FIELDS:
                    value = self._get_other_info(result, field)
                    if value: m[field.key] = value

                for field in self.PERSON_INFO_FIELDS:
                    value = self._get_person_info(result, field)
                    if value: m[field.key] = value

                Logger.info(self.get_logging(idx=ctr + 1, text=m))
                movies.append(m)

        self.search_results["movies"] = movies
