from fastapi.testclient import TestClient
from requests.exceptions import RequestException
from src.api import api
from src.scrape.base_scraper import BaseScraper
import pytest


client = TestClient(api)


def test_index() -> None:
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"detail": "A basic web scraper API for Filmarks Dramas."}


def test_invalid_endpoint() -> None:
    resp = client.get("/unknown")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not Found"}


def test_scrape_error_404(mocker) -> None:
    scrape_func = BaseScraper.scrape

    mocker.patch.object(
        target=BaseScraper,
        attribute="scrape",
        new=lambda endpoint, params: scrape_func(endpoint="test404", params={})
    )
    query = "test404"
    resp = client.get(f"/search/dramas?q={query}")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "The requested resource could not be found."}


def test_scrape_error_500(mocker) -> None:
    mocker.patch(
        target="src.scrape.search_drama_scraper.SearchDramaScraper.scrape", 
        side_effect=Exception("Testing - 500 Internal Server Error")
    )
    query = "test500"
    resp = client.get(f"/search/dramas?q={query}")

    assert resp.status_code == 500
    assert resp.json() == {"detail": "The server encountered an unexpected error."}


def test_scrape_error_503(mocker) -> None:
    mocker.patch(
        target="src.scrape.base_scraper.requests.get", 
        side_effect=RequestException("Testing - 503 Service Unavailable")
    )
    query = "test503"
    resp = client.get(f"/search/dramas?q={query}")

    assert resp.status_code == 503
    assert resp.json() == {"detail": "The service is currently unavailable."}


@pytest.mark.parametrize("query", ["", "?", "?q", "?q="])
def test_search_empty_query(query) -> None:
    resp = client.get(f"/search/dramas{query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["query"] == ""
    assert len(resp_data["results"]["dramas"]) == 0


def test_search_without_results() -> None:
    query = '".*&^'
    resp = client.get(f"/search/dramas?q={query}")
    resp_data = resp.json()
 
    assert resp.status_code == 200
    assert resp_data["query"] == '".*'
    assert len(resp_data["results"]["dramas"]) == 0


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "あなたの番です",
            "rating": 4.0,
            "mark_count": 29975,
            "clip_count": 6060,
            "series_id": 6055,
            "season_id": 8586,
            "link": "https://filmarks.com/dramas/6055/8586",
            "release_date": "2019年04月14日",
            "country_origin": "日本",
            "playback_time": "46分",
            "genre": ["ミステリー"],
            "scriptwriter": ["福原充則"],
            "cast": ["原田知世", "田中圭", "西野七瀬"],
        },
    ],
)
def test_search_with_results_single(test_data) -> None:
    query = "あなたの番です"
    resp = client.get(f"/search/dramas?q={query}")
    resp_data = resp.json()
    drama = resp_data["results"]["dramas"][0]

    assert resp.status_code == 200
    assert resp_data["query"] == query
    assert drama["title"] == test_data["title"]
    assert float(drama["rating"]) == pytest.approx(test_data["rating"], abs=0.5)
    assert drama["mark_count"] == pytest.approx(test_data["mark_count"], abs=1000)
    assert drama["clip_count"] == pytest.approx(test_data["clip_count"], abs=1000)
    assert drama["series_id"] == test_data["series_id"]
    assert drama["season_id"] == test_data["season_id"]
    assert drama["link"] == test_data["link"]
    assert "poster" in drama
    assert drama["release_date"] == test_data["release_date"]
    assert drama["is_airing"] is False
    assert drama["country_of_origin"] == test_data["country_origin"]
    assert drama["playback_time"] == test_data["playback_time"]
    assert drama["genre"] == test_data["genre"]
    assert "director" not in drama
    assert drama["scriptwriter"] == test_data["scriptwriter"]
    assert drama["cast"] == test_data["cast"]


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "ちはやふる－めぐり－",
            "series_id": 16234,
            "season_id": 21896,
            "link": "https://filmarks.com/dramas/16234/21896",
            "release_date": "2025年07月09日",
            "country_origin": "日本",
            "playback_time": "49分",
        },
        {
            "title": "ちはやふる ー繋ぐー",
            "series_id": 973,
            "season_id": 2117,
            "link": "https://filmarks.com/dramas/973/2117",
            "release_date": "2018年02月20日",
            "country_origin": "日本",
            "playback_time": "10分",
        },
    ],
)
def test_search_with_results_multiple(test_data) -> None:
    query = "ちはやふる"
    resp = client.get(f"/search/dramas?q={query}")
    resp_data = resp.json()
    drama = next(drama for drama in resp_data["results"]["dramas"] if drama["title"] == test_data["title"])

    assert resp.status_code == 200
    assert resp_data["query"] == query
    assert drama["title"] == test_data["title"]
    assert drama["series_id"] == test_data["series_id"]
    assert drama["season_id"] == test_data["season_id"]
    assert drama["link"] == test_data["link"]
    assert drama["release_date"] == test_data["release_date"]
    assert drama["country_of_origin"] == test_data["country_origin"]
    assert drama["playback_time"] == test_data["playback_time"]
