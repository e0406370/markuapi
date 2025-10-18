from pydantic import Field
from requests.exceptions import RequestException
from src.utility.models import ListParams, ReviewParams, SearchParams
from tests.conftest import get_json_val
import pytest


@pytest.mark.parametrize("path", [
    "/movies",
    "/movies//reviews",
    "/list-movie",
    "/list-movie/vod",
    "/list-movie/award",
    "/list-movie/year/2010s/2019",
    "/list-movie/year",
    "/list-movie/country",
    "/list-movie/genre",
    "/list-movie/distributor",
    "/list-movie/series",
    "/list-movie/tag",
    "/list-movie/person",
])
def test_invalid_endpoint_base(client_nc, path) -> None:
    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/movies/9999999999",
    "/movies/9999999999/reviews",
    "/movies/9999999999/reviews/9999999999",
    "/list-movie/vod/invalid_vod",
    "/list-movie/award/9999999999",
    "/list-movie/year/999s",
    "/list-movie/year/999",
    "/list-movie/country/9999999999",
    "/list-movie/genre/9999999999",
    "/list-movie/distributor/9999999999",
    "/list-movie/series/9999999999",
    "/list-movie/tag/invalid_tag",
    "/list-movie/person/9999999999",
])
def test_invalid_endpoint_filmarks(client_nc, path, caplog) -> None:
    resp = client_nc.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."
    assert "Invalid Filmarks page requested" in caplog.text


@pytest.mark.parametrize("test_data", [
    (
        "/search/movies?q=test500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to search movies."
    ),
    (
        "/movies/500",
        "src.scrape.info.info_movie_scraper.InfoMovieScraper.scrape",
        "Failed to retrieve information for movie with ID: 500."
    ),
    (
        "/movies/500/reviews",
        "src.scrape.info.info_movie_scraper.InfoMovieScraper.scrape",
        "Failed to retrieve reviews for movie with ID: 500."
    ),
    (
        "/movies/500/reviews/500",
        "src.scrape.info.info_movie_scraper.InfoMovieScraper.scrape",
        "Failed to retrieve review for movie with ID: 500 and review ID: 500."
    ),
    (
        "/list-movie/now",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch currently screening movies."
    ),
    (
        "/list-movie/coming-soon",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch upcoming movies."
    ),
    (
        "/list-movie/opening-this-week",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies opening this week."
    ),
    (
        "/list-movie/trend",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch trending movies."
    ),
    (
        "/list-movie/vod/500_vod",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies from VOD service: 500_vod."
    ),
    (
        "/list-movie/award/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies with award ID: 500."
    ),
    (
        "/list-movie/year/500s",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies from year series: 500s."
    ),
    (
        "/list-movie/year/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies from year: 500."
    ),
    (
        "/list-movie/country/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies with country ID: 500."
    ),
    (
        "/list-movie/genre/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies with genre ID: 500."
    ),
    (
        "/list-movie/distributor/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies with distributor ID: 500."
    ),
    (
        "/list-movie/series/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies with series ID: 500."
    ),
    (
        "/list-movie/tag/500_tag",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies with tag: 500_tag."
    ),
    (
        "/list-movie/person/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
        "Failed to fetch movies with person ID: 500."
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
    "/search/movies?q=test503",
    "/movies/503",
    "/movies/503/reviews",
    "/movies/503/reviews/503",
    "/list-movie/now",
    "/list-movie/coming-soon",
    "/list-movie/opening-this-week",
    "/list-movie/trend",
    "/list-movie/vod/503_vod",
    "/list-movie/award/503",
    "/list-movie/year/503s",
    "/list-movie/year/503",
    "/list-movie/country/503",
    "/list-movie/genre/503",
    "/list-movie/distributor/503",
    "/list-movie/series/503",
    "/list-movie/tag/503_tag",
    "/list-movie/person/503",
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
    "/movies/14348/reviews?page=9999999999999999999",
    "/list-movie/now?page=999999999999999999",
    "/list-movie/coming-soon?page=999999999999999999",
    "/list-movie/opening-this-week?page=999999999999999999",
    "/list-movie/trend?page=999999999999999999",
    "/list-movie/vod/prime_video?page=999999999999999999",
    "/list-movie/award/19?page=999999999999999999",
    "/list-movie/year/2010s?page=999999999999999999",
    "/list-movie/year/2001?page=999999999999999999",
    "/list-movie/country/5?page=999999999999999999",
    "/list-movie/genre/903?page=999999999999999999",
    "/list-movie/distributor/503?page=999999999999999999",
    "/list-movie/series/1?page=999999999999999999",
    "/list-movie/tag/洋画?page=999999999999999999",
    "/list-movie/person/93709?page=999999999999999999",
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
