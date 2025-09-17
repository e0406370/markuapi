from src.api import api
from tests.test_utils import client, get_json_val


def test_api_title() -> None:
    assert api.title == "MarkuAPI"


def test_api_version() -> None:
    assert api.version == "1.0.0"


def test_api_response() -> None:
    resp = client.get("/")

    assert resp.headers["content-type"] == "application/json"


def test_api_routes() -> None:
    defined_routes = {
        "/search/animes",
        "/animes/{anime_series_id}/{anime_season_id}",
        "/animes/{anime_series_id}/{anime_season_id}/reviews",
        "/list-anime/trend",
        "/list-anime/vod/{vod_name}",
        "/list-anime/year/{year_series}s",
        "/list-anime/year/{year}",
        "/list-anime/year/{year}/{season_id}",
        "/list-anime/company/{company_id}",
        "/list-anime/tag/{tag}",
        "/list-anime/person/{person_id}",
        "/search/dramas",
        "/dramas/{drama_series_id}/{drama_season_id}",
        "/dramas/{drama_series_id}/{drama_season_id}/reviews",
        "/list-drama/trend",
        "/list-drama/vod/{vod_name}",
        "/list-drama/year/{year_series}s",
        "/list-drama/year/{year}",
        "/list-drama/country/{country_id}",
        "/list-drama/genre/{genre_id}",
        "/list-drama/tag/{tag}",
        "/list-drama/person/{person_id}",
        "/search/movies",
        "/movies/{movie_id}",
        "/movies/{movie_id}/reviews",
        "/list-movie/now",
        "/list-movie/coming-soon",
        "/list-movie/opening-this-week",
        "/list-movie/trend",
        "/list-movie/vod/{vod_name}",
        "/list-movie/award/{award_id}",
        "/list-movie/year/{year_series}s",
        "/list-movie/year/{year}",
        "/list-movie/country/{country_id}",
        "/list-movie/genre/{genre_id}",
        "/list-movie/distributor/{distributor_id}",
        "/list-movie/series/{series_id}",
        "/list-movie/tag/{tag}",
        "/list-movie/person/{person_id}",
        "/",
    }
    special_routes = {
        "/openapi.json",
        "/docs",
        "/docs/oauth2-redirect",
        "/redoc",
    }

    route_cnt = 0
    for route in api.routes:
        if route.path not in special_routes:
            assert route.path in defined_routes
            route_cnt += 1

    assert route_cnt == len(defined_routes)


def test_index() -> None:
    resp = client.get("/")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.detail") == "Web scraper API for Filmarks Animes, Filmarks Dramas, and Filmarks Movies."


def test_unknown() -> None:
    resp = client.get("/unknown")
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"
