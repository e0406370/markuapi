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
def test_search_with_results(test_data) -> None:
    query = "あなたの番です"
    resp = client.get(f"/search/dramas?q={query}")
    resp_dramas = resp.json()["dramas"]

    assert resp.status_code == 200
    assert resp_dramas[0]["title"] == test_data["title"]
    assert float(resp_dramas[0]["rating"]) == pytest.approx(test_data["rating"], abs=0.5)
    assert resp_dramas[0]["mark_count"] == pytest.approx(test_data["mark_count"], abs=1000)
    assert resp_dramas[0]["clip_count"] == pytest.approx(test_data["clip_count"], abs=1000)
    assert resp_dramas[0]["series_id"] == test_data["series_id"]
    assert resp_dramas[0]["season_id"] == test_data["season_id"]
    assert resp_dramas[0]["link"] == test_data["link"]
    assert "poster" in resp_dramas[0]
    assert resp_dramas[0]["release_date"] == test_data["release_date"]
    assert resp_dramas[0]["is_airing"] is False
    assert resp_dramas[0]["country_origin"] == test_data["country_origin"]
    assert resp_dramas[0]["playback_time"] == test_data["playback_time"]
    assert resp_dramas[0]["genre"] == test_data["genre"]
    assert "director" not in resp_dramas[0]
    assert resp_dramas[0]["scriptwriter"] == test_data["scriptwriter"]
    assert resp_dramas[0]["cast"] == test_data["cast"]


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
