from fastapi.testclient import TestClient
from src.api import api
import pytest


client = TestClient(api)


def test_index() -> None:
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"message": "A basic web scraper API for Filmarks Dramas."}


def test_invalid_endpoint() -> None:
    resp = client.get("/unknown")

    assert resp.status_code == 404
    assert resp.json() == {"detail": "Not Found"}


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
    resp_dramas = resp.json()["dramas"]
    drama = resp_dramas[0]

    assert resp.status_code == 200
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
    assert drama["country_origin"] == test_data["country_origin"]
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
    resp_dramas = resp.json()["dramas"]
    drama = next(drama for drama in resp_dramas if drama["title"] == test_data["title"])

    assert resp.status_code == 200
    assert drama["title"] == test_data["title"]
    assert drama["series_id"] == test_data["series_id"]
    assert drama["season_id"] == test_data["season_id"]
    assert drama["link"] == test_data["link"]
    assert drama["release_date"] == test_data["release_date"]
    assert drama["country_origin"] == test_data["country_origin"]
    assert drama["playback_time"] == test_data["playback_time"]


def test_search_without_results() -> None:
    query = '".*&^'
    resp = client.get(f"/search/dramas?q={query}")
    resp_dramas = resp.json()["dramas"]

    assert resp.status_code == 200
    assert len(resp_dramas) == 0


def test_search_error(mocker) -> None:
    mocker.patch("src.api.search_dramas", side_effect=Exception("Testing - 500 Internal Server Error"))
    query = "test"
    resp = client.get(f"/search/dramas?q={query}")

    assert resp.status_code == 500
    assert resp.json() == {"message": "An unexpected error occurred."}


@pytest.mark.parametrize("query", ["", "?", "?q", "?q="])
def test_search_empty_query(query) -> None:
    resp = client.get(f"/search/dramas{query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert resp_data["query"] == ""
    assert len(resp_data["dramas"]) == 0
