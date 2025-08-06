from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet
from src.scrape.search_scraper import SearchScraper
from src.utility.lib import Logger, MsgSpecJSONResponse
from src.utility.models import DataClip, DataMark, Filmarks
from urllib.parse import urljoin
from typing import Dict, List


class SearchDramaScraper(SearchScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict) -> None:
        super().__init__(soup, params)

    def _is_results_empty(self) -> bool:
        condition = bool(self.soup.find("div", class_="p-timeline__zero"))
        if condition: Logger.warn(f"[0 | Query: {self.search_query} | Page: {self.page_number}] 一致する情報は見つかりませんでした。")

        return condition

    def _get_results_container(self) -> ResultSet[PageElement]:
        container = self.soup.find(
          "div", class_="p-contents-grid"
        ).find_all(
          "div", class_="js-cassette"
        )

        return container

    def _get_title(self, result: PageElement) -> str:
        return result.find("h3", class_="p-content-cassette__title").string

    def _get_rating(self, result: PageElement) -> str:
        return result.find("div", class_="c-rating__score").string

    def _get_data_mark(self, result: PageElement) -> DataMark:
        return MsgSpecJSONResponse.parse(content=result.attrs["data-mark"], type=DataMark)

    def _get_data_clip(self, result: PageElement) -> DataClip:
        return MsgSpecJSONResponse.parse(content=result.attrs["data-clip"], type=DataClip)

    def _get_poster(self, result: PageElement) -> str | None:
        poster_elem = result.find("div", class_="c2-poster-m").find("img")

        return poster_elem.attrs["src"] if poster_elem else None

    def _get_release_date(self, result: PageElement) -> str | None:
        title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="公開日：")

        return title_elem.find_next_sibling("span").string if title_elem else None

    def _is_airing(self, result: PageElement) -> bool:
        return bool(result.find("div", class_="c2-tag-broadcasting-now"))

    def _get_country_of_origin(self, result: PageElement) -> str | None:
        title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="製作国：")

        return title_elem.find_next("a").string if title_elem else None

    def _get_playback_time(self, result: PageElement) -> str | None:
        title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="再生時間：")

        return title_elem.find_next_sibling("span").string if title_elem else None

    def _get_genre(self, result: PageElement) -> List[str] | None:
        title_elem = result.find("h4", class_="p-content-cassette__genre-title")
        
        return [genre.string for genre in title_elem.find_next_sibling("ul").find_all("a")] if title_elem else None

    def _get_director(self, result: PageElement) -> List[str] | None:
        title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="監督")

        return [director.string for director in title_elem.find_next_sibling("ul").find_all("a")] if title_elem else None

    def _get_scriptwriter(self, result: PageElement) -> List[str] | None:
        title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="脚本")

        return [scriptwriter.string for scriptwriter in title_elem.find_next_sibling("ul").find_all("a")] if title_elem else None

    def _get_cast(self, result) -> List[str] | None:
        title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="出演者")

        return [cast.string for cast in title_elem.find_next_sibling("ul").find_all("a")] if title_elem else None

    def set_search_results(self) -> None:
        dramas = []
        
        if self._is_results_empty():
            self.search_results["dramas"] = dramas
            return

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

            d["link"] = urljoin(base=Filmarks.FILMARKS_BASE, url=Filmarks.InfoEP.DRAMAS.value.format(
                drama_series_id=data_clip.drama_series_id, 
                drama_season_id=data_clip.drama_season_id,
            ))

            if poster := self._get_poster(result):
                d["poster"] = poster

            if release_date := self._get_release_date(result):
                d["release_date"] = release_date  

            d["is_airing"] = self._is_airing(result)

            if country_of_origin := self._get_country_of_origin(result):
                d["country_of_origin"] = country_of_origin

            if playback_time := self._get_playback_time(result):
                d["playback_time"] = playback_time

            if genre := self._get_genre(result):
                d["genre"] = genre

            if director := self._get_director(result):
                d["director"] = director

            if scriptwriter := self._get_scriptwriter(result):
                d["scriptwriter"] = scriptwriter

            if cast := self._get_cast(result):
                d["cast"] = cast

            Logger.info(f"[{ctr + 1} | Query: {self.search_query} | Page: {self.page_number}] {str(d)}")
            dramas.append(d)

        self.search_results["dramas"] = dramas
