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


def test_search_without_results() -> None:
    query = '".*&^'
    resp = client.get(f"/search/dramas?q={query}")
    resp_dramas = resp.json()["dramas"]

    assert resp.status_code == 200
    assert len(resp_dramas) == 0
