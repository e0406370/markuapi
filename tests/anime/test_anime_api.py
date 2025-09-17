from pydantic import Field
from requests.exceptions import RequestException
from src.api import api
from src.scrape.base_scraper import BaseScraper
from src.utility.models import SearchParams
from tests.test_utils import client, get_json_val
import pytest


@pytest.mark.parametrize("path", [
    "/animes",
    "/animes/1",
    "/animes//1",
    "/animes/1//reviews"
    "/animes//1/reviews"
    "/list-anime",
    "/list-anime/vod",
    "/list-anime/year",
    "/list-anime/company",
    "/list-anime/tag",
    "/list-anime/person",
])
def test_invalid_endpoint_base(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/animes/9999999999/9999999999",
    "/animes/9999999999/9999999999/reviews",
    "/list-anime/vod/invalid_vod",
    "/list-anime/year/999s",
    "/list-anime/year/999",
    "/list-anime/year/2019/9",
    "/list-anime/company/9999999999",
    "/list-anime/tag/invalid_tag",
    "/list-anime/person/9999999999",
])
def test_invalid_endpoint_filmarks(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


@pytest.mark.parametrize("test_data", [
    (
        "/search/animes",
        {},
    ),
    (
        "/search/animes?q=デジモンアドベンチャー",
        {"path": "search/animes", "view": "anime"},
    ),
    (
        "/animes/2592/3304",
        {"path": "animes/{anime_series_id}/{anime_season_id}"},
    ),
    (
        "/animes/2592/3304/reviews",
        {"path": "animes/{anime_series_id}/{anime_season_id}/reviews", "type": "path"},
    ),
    (
        "/list-anime/trend",
        {"path": "list-anime/trend", "type": "query"},
    ),
    (
        "/list-anime/vod/prime_video",
        {"path": "list-anime/vod/{vod_name}", "type": "path", "view": "anime"},
    ),
    (
        "/list-anime/year/2020s",
        {"path": "list-anime/year/{year}s", "type": "path+query", "view": "anime"},
    ),
    (
        "/list-anime/year/2019",
        {"path": "list-anime/year/{year}", "type": "path+query", "view": "anime"},
    ),
    (
        "/list-anime/year/2019/1",
        {"path": "list-anime/year/{year}/{season}", "type": "path+query", "view": "anime"},
    ),
    (
        "/list-anime/company/41",
        '"path": "list-anime/company/{company_id}", "type": "path+query", "view": "anime"',
    ),
    (
        "/list-anime/tag/駄作",
        {"path": "list-anime/tag/{tag_id}", "type": "path+query", "view": "anime"},
    ),
    (
        "/list-anime/person/274563",
        {"path": "list-anime/person/{person}", "type": "path+query", "view": "anime"},
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
        "/search/animes?q=test500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/animes/500/500",
        "src.scrape.info.info_anime_scraper.InfoAnimeScraper.scrape",
    ),
    (
        "/animes/500/500/reviews",
        "src.scrape.info.info_anime_scraper.InfoAnimeScraper.scrape",
    ),
    (
        "/list-anime/trend",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/list-anime/vod/500_vod",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/list-anime/year/500s",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/list-anime/year/500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/list-anime/year/500/1",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/list-anime/company/500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/list-anime/tag/500_tag",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
    ),
    (
        "/list-anime/person/500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
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
    "/search/animes?q=test503",
    "/animes/503/503",
    "/animes/503/503/reviews",
    "/list-anime/trend",
    "/list-anime/vod/503_vod",
    "/list-anime/year/503s",
    "/list-anime/year/503",
    "/list-anime/year/503/1",
    "/list-anime/company/503",
    "/list-anime/tag/503_tag",
    "/list-anime/person/503",
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
    "/animes/2592/3304/reviews?page=9999999999999999999",
    "/list-anime/trend?page=999999999999999999",
    "/list-anime/vod/prime_video?page=999999999999999999",
    "/list-anime/year/2020s?page=999999999999999999",
    "/list-anime/year/2025?page=999999999999999999",
    "/list-anime/year/2019/1?page=999999999999999999",
    "/list-anime/year/2019/99",
    "/list-anime/company/41?page=999999999999999999",
    "/list-anime/tag/駄作?page=999999999999999999",
    "/list-anime/person/274563?page=999999999999999999",
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
