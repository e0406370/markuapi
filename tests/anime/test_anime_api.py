from pydantic import Field
from requests.exceptions import RequestException
from src.utility.models import ListParams, ReviewParams, SearchParams
from tests.conftest import get_json_val
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
def test_invalid_endpoint_base(client_nc, path) -> None:
    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/animes/9999999999/9999999999",
    "/animes/9999999999/9999999999/reviews",
    "/animes/9999999999/9999999999/reviews/9999999999",
    "/list-anime/vod/invalid_vod",
    "/list-anime/year/999s",
    "/list-anime/year/999",
    "/list-anime/year/2019/9",
    "/list-anime/company/9999999999",
    "/list-anime/tag/invalid_tag",
    "/list-anime/person/9999999999",
])
def test_invalid_endpoint_filmarks(client_nc, path, caplog) -> None:
    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."
    assert "Invalid Filmarks page requested" in caplog.text


@pytest.mark.parametrize("test_data", [
    (
        "/search/animes?q=test500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to search animes."
    ),
    (
        "/animes/500/500",
        "src.scrape.info.info_anime_scraper.InfoAnimeScraper.scrape",
        "Failed to retrieve information for anime with series ID: 500 and season ID: 500."
    ),
    (
        "/animes/500/500/reviews",
        "src.scrape.info.info_anime_scraper.InfoAnimeScraper.scrape",
        "Failed to retrieve reviews for anime with series ID: 500 and season ID: 500."
    ),
    (
        "/animes/500/500/reviews/500",
        "src.scrape.info.info_anime_scraper.InfoAnimeScraper.scrape",
        "Failed to retrieve review for anime with series ID: 500, season ID: 500, and review ID: 500."
    ),
    (
        "/list-anime/trend",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch trending animes."
    ),
    (
        "/list-anime/vod/500_vod",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch animes from VOD service: 500_vod."
    ),
    (
        "/list-anime/year/500s",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch animes from year series: 500s."
    ),
    (
        "/list-anime/year/500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch animes from year: 500."
    ),
    (
        "/list-anime/year/500/1",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch animes from year: 500 with season ID: 1."
    ),
    (
        "/list-anime/company/500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch animes with company ID: 500."
    ),
    (
        "/list-anime/tag/500_tag",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch animes with tag: 500_tag."
    ),
    (
        "/list-anime/person/500",
        "src.scrape.search.search_anime_scraper.SearchAnimeScraper.scrape",
        "Failed to fetch animes with person ID: 500."
    ),
])
def test_scrape_error_500_server_error(client_nc, mocker, test_data, caplog) -> None:
    mocker.patch(
        target=test_data[1],
        side_effect=Exception("Testing - 500 Internal Server Error"),
    )

    resp = client_nc.get(test_data[0])
    resp_data = resp.json()

    assert resp.status_code == 500
    assert get_json_val(resp_data, "$.detail") == "The server encountered an unexpected error."
    assert "Testing - 500 Internal Server Error" in caplog.text
    assert test_data[2] in caplog.text


@pytest.mark.parametrize("path", [
    "/search/animes?q=test503",
    "/animes/503/503",
    "/animes/503/503/reviews",
    "/animes/503/503/reviews/503",
    "/list-anime/trend",
    "/list-anime/vod/503_vod",
    "/list-anime/year/503s",
    "/list-anime/year/503",
    "/list-anime/year/503/1",
    "/list-anime/company/503",
    "/list-anime/tag/503_tag",
    "/list-anime/person/503",
])
def test_scrape_error_503_service_unavailable_session(client_nc, mocker, path, caplog) -> None:
    mocker.patch(
        target="src.scrape.base_scraper.Session",
        side_effect=RequestException("Testing - 503 Service Unavailable"),
    )

    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 503
    assert get_json_val(resp_data, "$.detail") == "The service is currently unavailable."
    assert "Request to Filmarks failed: 'Testing - 503 Service Unavailable'" in caplog.text 


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
def test_scrape_error_503_service_unavailable_filmarks(client_nc, path, caplog) -> None:
    class CustomParams():
        page: int = Field(1, gt=0)
    client_nc.app.dependency_overrides[SearchParams] = CustomParams
    client_nc.app.dependency_overrides[ReviewParams] = CustomParams
    client_nc.app.dependency_overrides[ListParams] = CustomParams

    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 503
    assert get_json_val(resp_data, "$.detail") == "The service is currently unavailable."
    assert "Filmarks is temporarily unavailable" in caplog.text

    del client_nc.app.dependency_overrides[SearchParams]
    del client_nc.app.dependency_overrides[ReviewParams]
    del client_nc.app.dependency_overrides[ListParams]
