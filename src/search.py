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
    soup = BeautifulSoup(html, "html.parser")
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

        d = {}
        d["title"] = title_elem.string
        d["rating"] = rating_elem.string
        d["mark_count"] = mark_count
        d["clip_count"] = clip_count
        d["series_id"] = drama_series_id
        d["season_id"] = drama_season_id
        d["link"] = FILMARKS_DRAMA.format(drama_series_id=drama_series_id, drama_season_id=drama_season_id)

        Logger.info(f"[{ctr + 1} | Query: {query}] {str(d)}")
        dramas.append(d)

    return dramas
