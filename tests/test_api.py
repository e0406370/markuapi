from requests.exceptions import RequestException
from src.scrape.base_scraper import BaseScraper
from tests.test_utils import client, get_json_val
import pytest


def test_index() -> None:
    resp = client.get("/")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.detail") == "A basic web scraper API for Filmarks Dramas."


@pytest.mark.parametrize("path", [
    "/unknown",
    "/dramas",
    "/dramas/1",
    "/dramas//1"
])
def test_invalid_endpoint_base(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


def test_invalid_endpoint_filmarks() -> None:
    resp = client.get("/dramas/9999999999/9999999999")
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


def test_scrape_error_404(mocker) -> None:
    scrape_func = BaseScraper.scrape
    mocker.patch.object(
        target=BaseScraper,
        attribute="scrape",
        new=lambda endpoint, params: scrape_func(endpoint="test404", params={})
    )

    query = "test404"
    resp = client.get(f"/search/dramas?q={query}")
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


def test_scrape_error_500(mocker) -> None:
    mocker.patch(
        target="src.scrape.search_drama_scraper.SearchDramaScraper.scrape", 
        side_effect=Exception("Testing - 500 Internal Server Error")
    )

    query = "test500"
    resp = client.get(f"/search/dramas?q={query}")
    resp_data = resp.json()

    assert resp.status_code == 500
    assert get_json_val(resp_data, "$.detail") == "The server encountered an unexpected error."


def test_scrape_error_503(mocker) -> None:
    mocker.patch(
        target="src.scrape.base_scraper.requests.get", 
        side_effect=RequestException("Testing - 503 Service Unavailable")
    )

    query = "test503"
    resp = client.get(f"/search/dramas?q={query}")
    resp_data = resp.json()

    assert resp.status_code == 503
    assert get_json_val(resp_data, "$.detail") == "The service is currently unavailable."
