from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet
from src.scrape.search_scraper import SearchScraper
from src.utility.lib import Logger, MsgSpecJSONResponse
from src.utility.models import DataClip, DataMark, Filmarks
from typing import Dict, List


class SearchDramaScraper(SearchScraper):
    def __init__(self, soup: BeautifulSoup, params: Dict) -> None:
        super().__init__(soup, params)

    def _is_results_empty(self) -> bool:
        condition = bool(self.soup.find("div", class_="p-timeline__zero"))
        if condition: Logger.warn(f"[0 | Query: {self.search_query} | Page: {self.page_number}] 一致する情報は見つかりませんでした。")

        return condition

    def _get_heading(self) -> str:
        return self.soup.select_one("h1.c-heading-1").text

    def _get_results_container(self) -> ResultSet[PageElement]:
        container = self.soup.find(
          "div", class_="p-contents-grid"
        ).find_all(
          "div", class_="js-cassette"
        )

        return container

    def _get_title(self, result: PageElement) -> str:
        return result.find("h3", class_="p-content-cassette__title").text

    def _get_rating(self, result: PageElement) -> float:
        rating = result.find("div", class_="c-rating__score").text

        return float(rating) if rating != "-" else rating

    def _get_data_mark(self, result: PageElement) -> DataMark:
        return MsgSpecJSONResponse.parse(content=result.attrs["data-mark"], type=DataMark)

    def _get_data_clip(self, result: PageElement) -> DataClip:
        return MsgSpecJSONResponse.parse(content=result.attrs["data-clip"], type=DataClip)

    def _get_poster(self, result: PageElement) -> str | None:
        poster = result.find("div", class_="c2-poster-m").find("img")

        return poster.attrs["src"] if poster else None
    
    def _get_other_info(self, result: PageElement, type: str) -> str | None:
        match type:
            case "release_date":
                title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="公開日：")

            case "country_of_origin":
                title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="製作国：")

            case "playback_time":
                title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="再生時間：")

            case _:
                raise ValueError("type can only be 'release_date', 'country_of_origin', or 'playback_time'!")

        match type:
            case "release_date" | "playback_time":
                return title_elem.find_next_sibling("span").text if title_elem else None

            case "country_of_origin":
                return title_elem.find_next("a").text if title_elem else None

    def _get_named_list(self, result: PageElement, type: str) -> List[str] | None:
        match type:
            case "genre":
                title_elem = result.find("h4", class_="p-content-cassette__genre-title")

            case "director":
                title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="監督")

            case "scriptwriter":
                title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="脚本")

            case "cast":
                title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="出演者")

            case _:
                raise ValueError("type can only be 'genre', 'director', 'scriptwriter', or 'cast'!")

        return [name.text for name in title_elem.find_next_sibling("ul").find_all("a")] if title_elem else None

    def set_search_results(self) -> None:
        self._raise_if_page_not_found()

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

            d["link"] = Filmarks.create_filmarks_link(Filmarks.Endpoints.INFO_DRAMAS.value["path"].format(
                drama_series_id=data_clip.drama_series_id, 
                drama_season_id=data_clip.drama_season_id,
            ))

            if poster := self._get_poster(result):
                d["poster"] = poster

            if release_date := self._get_other_info(result, "release_date"):
                d["release_date"] = release_date  

            if country_of_origin := self._get_other_info(result, "country_of_origin"):
                d["country_of_origin"] = country_of_origin

            if playback_time := self._get_other_info(result, "playback_time"):
                d["playback_time"] = playback_time

            if genre := self._get_named_list(result, "genre"):
                d["genre"] = genre

            if director := self._get_named_list(result, "director"):
                d["director"] = director

            if scriptwriter := self._get_named_list(result, "scriptwriter"):
                d["scriptwriter"] = scriptwriter

            if cast := self._get_named_list(result, "cast"):
                d["cast"] = cast

            Logger.info(f"[{ctr + 1} | Query: {self.search_query} | Page: {self.page_number}] {str(d)}")
            dramas.append(d)

        self.search_results["dramas"] = dramas
        self.search_heading = self._get_heading()
