import pytest
from src.utility.config import Config
from src.utility.endpoints import Endpoint
from tests.conftest import get_json_val


def test_api_metadata(client_nc) -> None:
    resp = client_nc.get("/openapi.json")
    resp_data = resp.json()

    assert get_json_val(resp_data, "$.openapi") == "3.1.0"
    assert get_json_val(resp_data, "$.info.title") == "MarkuAPI"
    assert get_json_val(resp_data, "$.info.summary") == "Web scraper API for Filmarks Animes, Filmarks Dramas, and Filmarks Movies."
    assert get_json_val(resp_data, "$.info.contact.name") == "e0406370"
    assert get_json_val(resp_data, "$.info.contact.url") == "https://github.com/e0406370/markuapi"
    assert get_json_val(resp_data, "$.info.version") == "1.1.0"
    assert get_json_val(resp_data, "$.tags[0].name") == "anime"
    assert get_json_val(resp_data, "$.tags[0].description") == "Endpoints for retrieving data from **[Filmarks Animes (フィルマークス・アニメ)](https://filmarks.com/animes)**"
    assert get_json_val(resp_data, "$.tags[1].name") == "drama"
    assert get_json_val(resp_data, "$.tags[1].description") == "Endpoints for retrieving data from **[Filmarks Dramas (フィルマークス・ドラマ)](https://filmarks.com/dramas)**"
    assert get_json_val(resp_data, "$.tags[2].name") == "movie"
    assert get_json_val(resp_data, "$.tags[2].description") == "Endpoints for retrieving data from **[Filmarks Movies (フィルマークス・映画)](https://filmarks.com)**"


def test_api_routes(client_nc) -> None:
    defined_routes = {
        "/search/animes",
        "/animes/{anime_series_id}/{anime_season_id}",
        "/animes/{anime_series_id}/{anime_season_id}/reviews",
        "/animes/{anime_series_id}/{anime_season_id}/reviews/{review_id}",
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
        "/dramas/{drama_series_id}/{drama_season_id}/reviews/{review_id}",
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
        "/movies/{movie_id}/reviews/{review_id}",
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
    seen_routes = set()

    for route in client_nc.app.routes:
        if route.path not in special_routes:
            assert route.path in defined_routes
            assert route.path not in seen_routes
            seen_routes.add(route.path)

    assert len(seen_routes) == len(defined_routes)
    assert len(seen_routes) == len(Endpoint) + 1


def test_api_index(client_nc) -> None:
    resp = client_nc.get("/")
    resp_data = resp.json()

    assert resp.headers["content-type"] == "application/json"
    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.detail") == "Web scraper API for Filmarks Animes, Filmarks Dramas, and Filmarks Movies."


def test_api_unknown(client_nc) -> None:
    resp = client_nc.get("/unknown")
    resp_data = resp.json()

    assert resp.status_code == 404
    assert get_json_val(resp_data, "$.detail") == "Not Found"


@pytest.mark.parametrize("path", [
    "/search/animes?q=デジモン",
    "/animes/2592/3304",
    "/animes/2592/3304/reviews",
    "/animes/1533/2046/reviews/292787",
    "/list-anime/trend",
    "/list-anime/vod/prime_video",
    "/list-anime/year/2020s",
    "/list-anime/year/2025",
    "/list-anime/year/2019/1",
    "/list-anime/company/41",
    "/list-anime/tag/駄作",
    "/list-anime/person/274563",
    "/search/dramas?q=あなたの番です",
    "/dramas/6055/8586",
    "/dramas/6055/8586/reviews",
    "/dramas/2767/4530/reviews/622799",
    "/list-drama/trend",
    "/list-drama/vod/prime_video",
    "/list-drama/year/2020s",
    "/list-drama/year/2025",
    "/list-drama/country/144",
    "/list-drama/genre/9",
    "/list-drama/tag/駄作",
    "/list-drama/person/25499",
    "/search/movies?q=ハリーポッター",
    "/movies/14348",
    "/movies/14348/reviews",
    "/movies/22767/reviews/230",
    "/list-movie/now",
    "/list-movie/coming-soon",
    "/list-movie/opening-this-week",
    "/list-movie/trend",
    "/list-movie/vod/prime_video",
    "/list-movie/award/19",
    "/list-movie/year/2010s",
    "/list-movie/year/2001",
    "/list-movie/country/5",
    "/list-movie/genre/903",
    "/list-movie/distributor/503",
    "/list-movie/series/1",
    "/list-movie/tag/洋画",
    "/list-movie/person/93709",
])
def test_api_without_cache(client_nc, path) -> None:
    resp_1 = client_nc.get(path)
    resp_1_data = resp_1.json()
    resp_1_scrape_date = get_json_val(resp_1_data, "$.scrape_date")

    resp_2 = client_nc.get(path)
    resp_2_data = resp_2.json()
    resp_2_scrape_date = get_json_val(resp_2_data, "$.scrape_date")

    assert resp_1.status_code == resp_2.status_code == 200
    assert resp_1_data != resp_2_data
    assert resp_1_scrape_date != resp_2_scrape_date


@pytest.mark.skipif(not Config.REDIS_ENABLE_CACHE, reason="requires Redis")
@pytest.mark.parametrize("path", [
    "/search/animes?q=デジモン",
    "/animes/2592/3304",
    "/animes/2592/3304/reviews",
    "/animes/1533/2046/reviews/292787",
    "/list-anime/trend",
    "/list-anime/vod/prime_video",
    "/list-anime/year/2020s",
    "/list-anime/year/2025",
    "/list-anime/year/2019/1",
    "/list-anime/company/41",
    "/list-anime/tag/駄作",
    "/list-anime/person/274563",
    "/search/dramas?q=あなたの番です",
    "/dramas/6055/8586",
    "/dramas/6055/8586/reviews",
    "/dramas/2767/4530/reviews/622799",
    "/list-drama/trend",
    "/list-drama/vod/prime_video",
    "/list-drama/year/2020s",
    "/list-drama/year/2025",
    "/list-drama/country/144",
    "/list-drama/genre/9",
    "/list-drama/tag/駄作",
    "/list-drama/person/25499",
    "/search/movies?q=ハリーポッター",
    "/movies/14348",
    "/movies/14348/reviews",
    "/movies/22767/reviews/230",
    "/list-movie/now",
    "/list-movie/coming-soon",
    "/list-movie/opening-this-week",
    "/list-movie/trend",
    "/list-movie/vod/prime_video",
    "/list-movie/award/19",
    "/list-movie/year/2010s",
    "/list-movie/year/2001",
    "/list-movie/country/5",
    "/list-movie/genre/903",
    "/list-movie/distributor/503",
    "/list-movie/series/1",
    "/list-movie/tag/洋画",
    "/list-movie/person/93709",
])
def test_api_with_cache(client_c, path) -> None:
    resp_1 = client_c.get(path)
    resp_1_data = resp_1.json()
    resp_1_scrape_date = get_json_val(resp_1_data, "$.scrape_date")

    resp_2 = client_c.get(path)
    resp_2_data = resp_2.json()
    resp_2_scrape_date = get_json_val(resp_2_data, "$.scrape_date")

    assert resp_1.status_code == resp_2.status_code == 200
    assert resp_1_data == resp_2_data
    assert resp_1_scrape_date == resp_2_scrape_date


@pytest.mark.parametrize("path", [
    "/search/animes?q=デジモン",
    "/animes/2592/3304",
    "/animes/2592/3304/reviews",
    "/animes/1533/2046/reviews/292787",
    "/list-anime/trend",
    "/list-anime/vod/prime_video",
    "/list-anime/year/2020s",
    "/list-anime/year/2025",
    "/list-anime/year/2019/1",
    "/list-anime/company/41",
    "/list-anime/tag/駄作",
    "/list-anime/person/274563",
    "/search/dramas?q=あなたの番です",
    "/dramas/6055/8586",
    "/dramas/6055/8586/reviews",
    "/dramas/2767/4530/reviews/622799",
    "/list-drama/trend",
    "/list-drama/vod/prime_video",
    "/list-drama/year/2020s",
    "/list-drama/year/2025",
    "/list-drama/country/144",
    "/list-drama/genre/9",
    "/list-drama/tag/駄作",
    "/list-drama/person/25499",
    "/search/movies?q=ハリーポッター",
    "/movies/14348",
    "/movies/14348/reviews",
    "/movies/22767/reviews/230",
    "/list-movie/now",
    "/list-movie/coming-soon",
    "/list-movie/opening-this-week",
    "/list-movie/trend",
    "/list-movie/vod/prime_video",
    "/list-movie/award/19",
    "/list-movie/year/2010s",
    "/list-movie/year/2001",
    "/list-movie/country/5",
    "/list-movie/genre/903",
    "/list-movie/distributor/503",
    "/list-movie/series/1",
    "/list-movie/tag/洋画",
    "/list-movie/person/93709",
])
def test_api_with_cache_connection_error(client_c_conn_err, path) -> None:
    resp_1 = client_c_conn_err.get(path)
    resp_1_data = resp_1.json()
    resp_1_scrape_date = get_json_val(resp_1_data, "$.scrape_date")

    resp_2 = client_c_conn_err.get(path)
    resp_2_data = resp_2.json()
    resp_2_scrape_date = get_json_val(resp_2_data, "$.scrape_date")

    assert resp_1.status_code == resp_2.status_code == 200
    assert resp_1_data != resp_2_data
    assert resp_1_scrape_date != resp_2_scrape_date


@pytest.mark.parametrize("path", [
    "/search/animes?q=デジモン",
    "/animes/2592/3304",
    "/animes/2592/3304/reviews",
    "/animes/1533/2046/reviews/292787",
    "/list-anime/trend",
    "/list-anime/vod/prime_video",
    "/list-anime/year/2020s",
    "/list-anime/year/2025",
    "/list-anime/year/2019/1",
    "/list-anime/company/41",
    "/list-anime/tag/駄作",
    "/list-anime/person/274563",
    "/search/dramas?q=あなたの番です",
    "/dramas/6055/8586",
    "/dramas/6055/8586/reviews",
    "/dramas/2767/4530/reviews/622799",
    "/list-drama/trend",
    "/list-drama/vod/prime_video",
    "/list-drama/year/2020s",
    "/list-drama/year/2025",
    "/list-drama/country/144",
    "/list-drama/genre/9",
    "/list-drama/tag/駄作",
    "/list-drama/person/25499",
    "/search/movies?q=ハリーポッター",
    "/movies/14348",
    "/movies/14348/reviews",
    "/movies/22767/reviews/230",
    "/list-movie/now",
    "/list-movie/coming-soon",
    "/list-movie/opening-this-week",
    "/list-movie/trend",
    "/list-movie/vod/prime_video",
    "/list-movie/award/19",
    "/list-movie/year/2010s",
    "/list-movie/year/2001",
    "/list-movie/country/5",
    "/list-movie/genre/903",
    "/list-movie/distributor/503",
    "/list-movie/series/1",
    "/list-movie/tag/洋画",
    "/list-movie/person/93709",
])
def test_api_with_cache_server_error(client_c_serv_err, path) -> None:    
    resp_1 = client_c_serv_err.get(path)
    resp_1_data = resp_1.json()
    resp_1_scrape_date = get_json_val(resp_1_data, "$.scrape_date")

    resp_2 = client_c_serv_err.get(path)
    resp_2_data = resp_2.json()
    resp_2_scrape_date = get_json_val(resp_2_data, "$.scrape_date")

    assert resp_1.status_code == resp_2.status_code == 200
    assert resp_1_data != resp_2_data
    assert resp_1_scrape_date != resp_2_scrape_date
