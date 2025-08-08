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
    "/search",
    "/dramas",
    "/dramas/1",
    "/dramas//1",
    "/list-drama",
    "/list-drama/country",
    "/list-drama/year",
])
def test_invalid_endpoint_base(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/dramas/9999999999/9999999999",
    "/list-drama/country/9999999999",
    "/list-drama/year/999",
])
def test_invalid_endpoint_filmarks(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


@pytest.mark.parametrize("test_data", [
    (
        "/search/dramas?q=test503", 
        {},
    ),
    (
        "/dramas/404/404", 
        {"type": "query" , "path": "404"},
    ),
    (
        "/list-drama/trend", 
        {"type": "404", "path": "list-drama/trend"},
    ),
    (
        "/list-drama/country/404", 
        {"type": "path"},
    ),
    (
        "/list-drama/year/404", 
        {"type": "path+query", "path": "404"},
    ),
])
def test_scrape_error_404(mocker, test_data) -> None:
    scrape_func = BaseScraper.scrape
    mocker.patch.object(
        target=BaseScraper,
        attribute="scrape",
        new=lambda endpoint, req: scrape_func(endpoint=test_data[1], req=None)
    )

    resp = client.get(test_data[0])
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


@pytest.mark.parametrize("test_data", [
    (
        "/search/dramas?q=test500",
        "src.scrape.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/dramas/500/500",
        "src.scrape.info_drama_scraper.InfoDramaScraper.scrape",
    ),
    (
        "/list-drama/trend",
        "src.scrape.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/country/500",
        "src.scrape.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/year/500",
        "src.scrape.search_drama_scraper.SearchDramaScraper.scrape",
    ),
])
def test_scrape_error_500(mocker, test_data) -> None:
    mocker.patch(
        target=test_data[1], 
        side_effect=Exception("Testing - 500 Internal Server Error")
    )

    resp = client.get(test_data[0])
    resp_data = resp.json()

    assert resp.status_code == 500
    assert get_json_val(resp_data, "$.detail") == "The server encountered an unexpected error."


@pytest.mark.parametrize("path", [
    "/search/dramas?q=test503",
    "/dramas/503/503",
    "/list-drama/trend",
    "/list-drama/country/503",
    "/list-drama/year/503",
])
def test_scrape_error_503(mocker, path) -> None:
    mocker.patch(
        target="src.scrape.base_scraper.requests.Session", 
        side_effect=RequestException("Testing - 503 Service Unavailable")
    )

    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 503
    assert get_json_val(resp_data, "$.detail") == "The service is currently unavailable."
