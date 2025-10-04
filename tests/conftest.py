from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from jsonpath_ng import parse
from redis.exceptions import ConnectionError
from requests import get
from src.api import init_api
from src.utility.utils import Utils
from typing import Any, Optional
import pytest

ANIME_ENG = "[anime]"
DRAMA_ENG = "[drama]"
MOVIE_ENG = "[movie]"

ANIME_JPN = "アニメ"
DRAMA_JPN = "ドラマ"
MOVIE_JPN = "映画"


@pytest.fixture(scope="function")
def client_nc():
    api = init_api(enable_cache=False, flush_cache=False)

    with TestClient(api) as client:
        yield client


@pytest.fixture(scope="function")
def client_c():
    api = init_api(enable_cache=True, flush_cache=True)

    with TestClient(api) as client:
        yield client


@pytest.fixture(scope="function")
def client_c_conn_err(mocker):
    mock_redis = mocker.MagicMock()
    mock_redis.ping.side_effect = ConnectionError

    mocker.patch(
        target="src.utility.rediss.aioredis.from_url",
        return_value=mock_redis
    )

    api = init_api(enable_cache=True, flush_cache=False)

    with TestClient(api) as client:
        yield client


@pytest.fixture(scope="function")
def client_c_serv_err(mocker):
    mock_redis = mocker.MagicMock()
    mock_redis.ping.side_effect = Exception

    mocker.patch(
        target="src.utility.rediss.aioredis.from_url",
        return_value=mock_redis
    )

    api = init_api(enable_cache=True, flush_cache=False)

    with TestClient(api) as client:
        yield client


def get_json_val(json: Any, path: str) -> Optional[Any]:
    query = parse(path)
    match = query.find(json)

    return match[0].value if match else None


def get_reviews_last_page(slug: str) -> int:
    resp = get(url=f"{Utils.FILMARKS_BASE}{slug}", headers=Utils.FILMARKS_REQUEST_HEADERS)
    soup = BeautifulSoup(resp.text, "lxml")

    last = soup.select_one("div.p-timeline a.c2-pagination__last")
    return 1 if not last else int(last.attrs["href"].split("?page=")[-1])
