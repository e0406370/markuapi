from pydantic import Field
from requests.exceptions import RequestException
from src.utility.models import ListParams, ReviewParams, SearchParams
from tests.conftest import get_json_val
import pytest


@pytest.mark.parametrize("path", [
    "/dramas",
    "/dramas/1",
    "/dramas//1",
    "/dramas/1//reviews",
    "/dramas//1/reviews",
    "/list-drama",
    "/list-drama/vod",
    "/list-drama/year/2010s/2019",
    "/list-drama/year",
    "/list-drama/country",
    "/list-drama/genre",
    "/list-drama/tag",
    "/list-drama/person",
])
def test_invalid_endpoint_base(client_nc, path) -> None:
    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/dramas/9999999999/9999999999",
    "/dramas/9999999999/9999999999/reviews",
    "/list-drama/vod/invalid_vod",
    "/list-drama/year/999s",
    "/list-drama/year/999",
    "/list-drama/country/9999999999",
    "/list-drama/genre/9999999999",
    "/list-drama/tag/invalid_tag",
    "/list-drama/person/9999999999",
])
def test_invalid_endpoint_filmarks(client_nc, path, caplog) -> None:
    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."
    assert "Invalid Filmarks page requested" in caplog.text


@pytest.mark.parametrize("test_data", [
    (
        "/search/dramas?q=test500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to search dramas."
    ),
    (
        "/dramas/500/500",
        "src.scrape.info.info_drama_scraper.InfoDramaScraper.scrape",
        "Failed to retrieve information for drama with series ID: 500 and season ID: 500."
    ),
    (
        "/dramas/500/500/reviews",
        "src.scrape.info.info_drama_scraper.InfoDramaScraper.scrape",
        "Failed to retrieve reviews for drama with series ID: 500 and season ID: 500."
    ),
    (
        "/list-drama/trend",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch trending dramas."
    ),
    (
        "/list-drama/vod/500_vod",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch dramas from VOD service: 500_vod."
    ),
    (
        "/list-drama/year/500s",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch dramas from year series: 500s."
    ),
    (
        "/list-drama/year/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch dramas from year: 500."
    ),
    (
        "/list-drama/country/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch dramas with country ID: 500."
    ),
    (
        "/list-drama/genre/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch dramas with genre ID: 500."
    ),
    (
        "/list-drama/tag/500_tag",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch dramas with tag: 500_tag."
    ),
    (
        "/list-drama/person/500",
        "src.scrape.search.search_drama_scraper.SearchDramaScraper.scrape",
        "Failed to fetch dramas with person ID: 500."
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
    "/search/dramas?q=test503",
    "/dramas/503/503",
    "/dramas/503/503/reviews",
    "/list-drama/trend",
    "/list-drama/vod/503_vod",
    "/list-drama/year/503s",
    "/list-drama/year/503",
    "/list-drama/country/503",
    "/list-drama/genre/503",
    "/list-drama/tag/503_tag",
    "/list-drama/person/503",
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
    "/dramas/6055/8586/reviews?page=9999999999999999999",
    "/list-drama/trend?page=999999999999999999",
    "/list-drama/vod/prime_video?page=999999999999999999",
    "/list-drama/year/2020s?page=999999999999999999",
    "/list-drama/year/2025?page=999999999999999999",
    "/list-drama/country/144?page=999999999999999999",
    "/list-drama/genre/9?page=999999999999999999",
    "/list-drama/tag/駄作?page=999999999999999999",
    "/list-drama/person/25499?page=999999999999999999",
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

