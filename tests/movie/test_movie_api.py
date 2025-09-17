from pydantic import Field
from requests.exceptions import RequestException
from src.api import api
from src.scrape.base_scraper import BaseScraper
from src.utility.models import SearchParams
from tests.test_utils import client, get_json_val
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
def test_invalid_endpoint_base(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/movies/9999999999",
    "/movies/9999999999/reviews",
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
def test_invalid_endpoint_filmarks(path) -> None:
    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "The requested resource could not be found."


@pytest.mark.parametrize("test_data", [
    (
        "/search/movies",
        {},
    ),
    (
        "/search/movies?q=ハリーポッター",
        {"path": "search/movies", "view": "movie"},
    ),
    (
        "/movies/14348",
        {"path": "movies/{movie_id}"},
    ),
    (
        "/movies/14348/reviews",
        {"path": "movies/{movie_id}/reviews", "type": "path"},
    ),
    (
        "/list-movie/now",
        {"path": "list/now", "type": "query"},
    ),
    (
        "/list-movie/coming-soon",
        {"path": "list/coming", "type": "query"},
    ),
    (
        "/list-movie/opening-this-week",
        {"path": "list/upcoming", "type": "query"},
    ),
    (
        "/list-movie/trend",
        {"path": "list/trend", "type": "query"},
    ),
    (
        "/list-movie/vod/prime_video",
        {"path": "list/vod/{vod_name}", "type": "path", "view": "movie"},
    ),
    (
        "/list-movie/award/19",
        {"path": "list/award/{award_id}", "type": "path", "view": "movie"},
    ),
    (
        "/list-movie/year/2010s",
        {"path": "list/year/{year}s", "type": "path+query", "view": "movie"},
    ),
    (
        "/list-movie/year/2001",
        {"path": "list/year/{year}", "type": "path+query", "view": "movie"},
    ),
    (
        "/list-movie/country/5",
        '"path": "list/country/{country_id}", "type": "path+query", "view": "movie"',
    ),
    (
        "/list-movie/genre/903",
        {"type": "path+query"},
    ),
    (
        "/list-movie/distributor/503",
        '"path": "list/distributor/{distributor_id}", "type": "path+query", "view": "movie"',
    ),
    (
        "/list-movie/series/1",
        '"path": "list/series/{series_id}", "type": "path+query", "view": "movie"',
    ),
    (
        "/list-movie/tag/洋画",
        {"path": "list-movie/tag/{tag_id}", "type": "path+query", "view": "movie"},
    ),
    (
        "/list-movie/person/93709",
        {"path": "list-movie/person/{person}", "type": "path+query", "view": "movie"},
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
        "/search/movies?q=test500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/movies/500",
        "src.scrape.info.info_movie_scraper.InfoMovieScraper.scrape",
    ),
    (
        "/movies/500/reviews",
        "src.scrape.info.info_movie_scraper.InfoMovieScraper.scrape",
    ),
    (
        "/list-movie/now",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/coming-soon",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/opening-this-week",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/trend",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/vod/500_vod",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/award/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/year/500s",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/year/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/country/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/genre/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/distributor/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/series/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/tag/500_tag",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
    ),
    (
        "/list-movie/person/500",
        "src.scrape.search.search_movie_scraper.SearchMovieScraper.scrape",
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
    "/search/movies?q=test503",
    "/movies/503",
    "/movies/503/reviews",
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
def test_scrape_error_503_service_unavailable_filmarks(path) -> None:
    class CustomSearchParams(SearchParams):
        page: int = Field(1, gt=0)
    api.dependency_overrides[SearchParams] = CustomSearchParams

    resp = client.get(path)
    resp_data = resp.json()

    assert resp.status_code == 503
    assert get_json_val(resp_data, "$.detail") == "The service is currently unavailable."

    del api.dependency_overrides[SearchParams]
