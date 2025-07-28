import json
from bs4 import BeautifulSoup
from lib import Logger
from urllib import parse
from urllib.request import Request, urlopen
from typing import List


FILMARKS_SEARCH = "https://filmarks.com/search/dramas?q={query}"
FILMARKS_DRAMA = "https://filmarks.com/dramas/{drama_series_id}/{drama_season_id}"


def search_dramas(query: str) -> List[str]:
    req = Request(FILMARKS_SEARCH.format(query=parse.quote(query)))
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")

    if soup.find("div", class_="p-timeline__zero"):
        Logger.warn(f"[0 | Query: {query}] 一致する情報は見つかりませんでした。")
        return []

    results = soup.find("div", class_="p-contents-grid").find_all(
        "div", class_="js-cassette"
    )

    ctr = 0
    dramas = []

    for result in results:
        if ctr == 10: break

        title_elem = result.find("h3", class_="p-content-cassette__title")
        rating_elem = result.find("div", class_="c-rating__score")

        data_elem = json.loads(result.attrs["data-clip"])
        drama_series_id = data_elem["drama_series_id"]
        drama_season_id = data_elem["drama_season_id"]

        d = {}
        d["title"] = title_elem.string
        d["rating"] = rating_elem.string
        d["link"] = FILMARKS_DRAMA.format(drama_series_id=drama_series_id, drama_season_id=drama_season_id)

        Logger.info(f"[{ctr + 1} | Query: {query}] {str(d)}")
        dramas.append(d)
        ctr += 1

    return dramas 
