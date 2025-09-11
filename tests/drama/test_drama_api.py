from pydantic import Field
from requests.exceptions import RequestException
from src.api import api
from src.scrape.base_scraper import BaseScraper
from src.utility.models import SearchParams
from tests.test_utils import client, get_json_val
import pytest


@pytest.mark.parametrize("path", [
    "/dramas",
    "/dramas/1",
    "/dramas//1",
    "/list-drama",
    "/list-drama/vod",
    "/list-drama/year/2010s/2019",
    "/list-drama/year",
    "/list-drama/country",
    "/list-drama/genre",
    "/list-drama/tag",
    "/list-drama/person",
])
def test_invalid_endpoint_base(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/dramas/9999999999/9999999999",
    "/list-drama/vod/invalid_vod",
    "/list-drama/year/999s",
    "/list-drama/year/999",
    "/list-drama/country/9999999999",
    "/list-drama/genre/9999999999",
    "/list-drama/tag/invalid_tag",
    "/list-drama/person/9999999999",
])
def test_invalid_endpoint_filmarks(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


@pytest.mark.parametrize("test_data", [
    (
        "/search/dramas",
        {},
    ),
    (
        "/search/dramas?q=あなたの番です",
        {"path": "search/dramas", "view": "drama"},
    ),
    (
        "/dramas/6055/8586",
        {"path": "dramas/{drama_series_id}/{drama_season_id}"},
    ),
    (
        "/list-drama/trend",
        {"path": "list-drama/trend", "type": "query"},
    ),
    (
        "/list-drama/vod/prime_video",
        {"path": "list-drama/vod/{vod_name}", "type": "path", "view": "drama"},
    ),
    (
        "/list-drama/year/2020s",
        {"path": "list-drama/year/{year}s", "type": "path+query", "view": "drama"},
    ),
    (
        "/list-drama/year/2020",
        {"path": "list-drama/year/{year}", "type": "path+query", "view": "drama"},
    ),
    (
        "/list-drama/country/144",
        '"path": "list-drama/country/{country_id}", "type": "path+query", "view": "drama"',
    ),
    (
        "/list-drama/genre/9",
        {"type": "path+query"},
    ),
    (
        "/list-drama/tag/駄作",
        {"path": "list-drama/tag/{tag_id}", "type": "path+query", "view": "drama"},
    ),
    (
        "/list-drama/person/25499",
        {"path": "list-drama/person/{person}", "type": "path+query", "view": "drama"},
    ),
])
def test_scrape_error_404_not_found(mocker, test_data) -> None:
    scrape_func = BaseScraper.scrape
    mocker.patch.object(
        target=BaseScraper,
        attribute="scrape",
        new=lambda endpoint, req: scrape_func(endpoint=test_data[1], req=None),
    )

    resp = client.get(test_data[0])
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


@pytest.mark.parametrize("test_data", [
    (
        "/search/dramas?q=test500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/dramas/500/500",
        "src.scrape.info.info_drama_scraper.InfoDramaScraper.scrape",
    ),
    (
        "/list-drama/trend",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/vod/500_vod",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/year/500s",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/year/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/country/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/genre/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/tag/500_tag",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
    (
        "/list-drama/person/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
    ),
])
def test_scrape_error_500_server_error(mocker, test_data) -> None:
    mocker.patch(
        target=test_data[1],
        side_effect=Exception("Testing - 500 Internal Server Error"),
    )

    resp = client.get(test_data[0])
    resp_data = resp.json()

    assert resp.status_code == 500
    assert get_json_val(resp_data, "$.detail") == "The server encountered an unexpected error."


@pytest.mark.parametrize("path", [
    "/search/dramas?q=test503",
    "/dramas/503/503",
    "/list-drama/trend",
    "/list-drama/vod/503_vod",
    "/list-drama/year/503s",
    "/list-drama/year/503",
    "/list-drama/country/503",
    "/list-drama/genre/503",
    "/list-drama/tag/503_tag",
    "/list-drama/person/503",
])
def test_scrape_error_503_service_unavailable_session(mocker, path) -> None:
    mocker.patch(
        target="src.scrape.base_scraper.Session",
        side_effect=RequestException("Testing - 503 Service Unavailable"),
    )

    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 503
    assert get_json_val(resp_data, "$.detail") == "The service is currently unavailable."


@pytest.mark.parametrize("path", [
    "/list-drama/trend?page=999999999999999999",
    "/list-drama/vod/prime_video?page=999999999999999999",
    "/list-drama/year/2020s?page=999999999999999999",
    "/list-drama/year/2025?page=999999999999999999",
    "/list-drama/country/144?page=999999999999999999",
    "/list-drama/genre/9?page=999999999999999999",
    "/list-drama/tag/駄作?page=999999999999999999",
    "/list-drama/person/25499?page=999999999999999999",
])
def test_scrape_error_503_service_unavailable_filmarks(path) -> None:
    class CustomSearchParams(SearchParams):
        page: int = Field(1, gt=0)
    api.dependency_overrides[SearchParams] = CustomSearchParams

    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 503
    assert get_json_val(resp_data, "$.detail") == "The service is currently unavailable."

    del api.dependency_overrides[SearchParams]
