from bs4 import BeautifulSoup
from src.lib import Logger, MsgSpecJSONResponse
from urllib import parse
from urllib.request import Request, urlopen
from typing import Dict, List


FILMARKS_SEARCH = "https://filmarks.com/search/dramas?q={query}"
FILMARKS_DRAMA = "https://filmarks.com/dramas/{drama_series_id}/{drama_season_id}"


def search_dramas(query: str) -> List[Dict[str, str]]:
    req = Request(FILMARKS_SEARCH.format(query=parse.quote(query)))
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "lxml")
    dramas = []

    if soup.find("div", class_="p-timeline__zero"):
        Logger.warn(f"[0 | Query: {query}] 一致する情報は見つかりませんでした。")
        return dramas

    results = soup.find(
        "div", class_="p-contents-grid"
    ).find_all(
        "div", class_="js-cassette"
    )

    for ctr, result in enumerate(results[:10]):
        title_elem = result.find("h3", class_="p-content-cassette__title")
        rating_elem = result.find("div", class_="c-rating__score")

        data_mark_elem = MsgSpecJSONResponse.parse(result.attrs["data-mark"])
        mark_count = data_mark_elem["count"]

        data_clip_elem = MsgSpecJSONResponse.parse(result.attrs["data-clip"])
        drama_series_id = data_clip_elem["drama_series_id"]
        drama_season_id = data_clip_elem["drama_season_id"]
        clip_count = data_clip_elem["count"]

        poster_elem = result.find("div", class_="c2-poster-m").find("img")

        release_date_title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="公開日：")
        release_date_elem = release_date_title_elem.find_next_sibling("span") if release_date_title_elem else None

        is_airing_elem = result.find("div", class_="c2-tag-broadcasting-now")

        country_origin_title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="製作国：")
        country_origin_elem = country_origin_title_elem.find_next("a") if country_origin_title_elem else None

        playback_time_title_elem = result.find("h4", class_="p-content-cassette__other-info-title", string="再生時間：")
        playback_time_elem = playback_time_title_elem.find_next_sibling("span") if playback_time_title_elem else None

        genre_title_elem = result.find("h4", class_="p-content-cassette__genre-title")
        genre_elem = genre_title_elem.find_next_sibling("ul") if genre_title_elem else None

        director_title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="監督")
        director_elem = director_title_elem.find_next_sibling("ul") if director_title_elem else None

        scriptwriter_title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="脚本")
        scriptwriter_elem = scriptwriter_title_elem.find_next_sibling("ul") if scriptwriter_title_elem else None

        cast_title_elem = result.find("h4", class_="p-content-cassette__people-list-term", string="出演者")
        cast_elem = cast_title_elem.find_next_sibling("ul") if cast_title_elem else None

        d = {}
        d["title"] = title_elem.string
        d["rating"] = rating_elem.string
        d["mark_count"] = mark_count
        d["clip_count"] = clip_count
        d["series_id"] = drama_series_id
        d["season_id"] = drama_season_id
        d["link"] = FILMARKS_DRAMA.format(drama_series_id=drama_series_id, drama_season_id=drama_season_id)
        if poster_elem: d["poster"] = poster_elem.attrs["src"]
        if release_date_elem: d["release_date"] = release_date_elem.string
        d["is_airing"] = True if is_airing_elem else False
        if country_origin_elem: d["country_origin"] = country_origin_elem.string
        if playback_time_elem: d["playback_time"] = playback_time_elem.string
        if genre_elem: d["genre"] = [genre.string for genre in genre_elem.find_all("a")]
        if director_elem: d["director"] = [director.string for director in director_elem.find_all("a")]
        if scriptwriter_elem: d["scriptwriter"] = [scriptwriter.string for scriptwriter in scriptwriter_elem.find_all("a")]
        if cast_elem: d["cast"] = [cast.string for cast in cast_elem.find_all("a")]

        Logger.info(f"[{ctr + 1} | Query: {query}] {str(d)}")
        dramas.append(d)

    return dramas
