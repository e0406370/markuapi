from tests.test_utils import client, get_json_val
import json
import pytest

list_routes = {
    "now": "/list-movie/now",
    "coming-soon": "/list-movie/coming-soon",
    "opening-this-week": "/list-movie/opening-this-week",
    "trend": "/list-movie/trend",
    "vod": "/list-movie/vod/{vod_name}",
    "award": "/list-movie/award/{award_id}",
    "year_series": "/list-movie/year/{year_series}s",
    "year_specific": "/list-movie/year/{year}",
    "country": "/list-movie/country/{country_id}",
    "genre": "/list-movie/genre/{genre_id}",
    "distributor": "/list-movie/distributor/{distributor_id}",
    "series": "/list-movie/series/{series_id}",
    "tag": "/list-movie/tag/{tag}",
    "person": "/list-movie/person/{person_id}",
}


@pytest.mark.parametrize("query", [
    "?limit",
    "?limit=", 
    "?limit=xyz123",
    "?limit=１０",
    "?page",
    "?page=", 
    "?page=987abc",
    "?page=５",
    "?limit=1&page=#",
    "?limit=@&page=1",
])
def test_list_query_params_not_valid_integer(query) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "award":
                route = route.format(award_id="19")
            case "year_series":
                route = route.format(year_series="2010")
            case "year_specific":
                route = route.format(year="2001")
            case "country":
                route = route.format(country_id="5")
            case "genre":
                route = route.format(genre_id="903")
            case "distributor":
                route = route.format(distributor_id="503")
            case "series":
                route = route.format(series_id="1")
            case "tag":
                route = route.format(tag="洋画")
            case "person":
                route = route.format(person_id="93709")
            case _:
                pass

        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize("query", [
    "?limit=-1",
    "?limit=0",
    "?page=-5", 
    "?page=0",
    "?limit=-3&page=3",
    "?limit=1&page=0",
])
def test_list_query_params_less_than_min_threshold(query) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "award":
                route = route.format(award_id="19")
            case "year_series":
                route = route.format(year_series="2010")
            case "year_specific":
                route = route.format(year="2001")
            case "country":
                route = route.format(country_id="5")
            case "genre":
                route = route.format(genre_id="903")
            case "distributor":
                route = route.format(distributor_id="503")
            case "series":
                route = route.format(series_id="1")
            case "tag":
                route = route.format(tag="洋画")
            case "person":
                route = route.format(person_id="93709")
            case _:
                pass

        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be greater than 0"


@pytest.mark.parametrize("query", [
    "?limit=101",
    "?page=2001",
    "?limit=101&page=3",
    "?limit=100&page=2001",
])
def test_list_query_params_more_than_max_threshold(query) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "award":
                route = route.format(award_id="19")
            case "year_series":
                route = route.format(year_series="2010")
            case "year_specific":
                route = route.format(year="2001")
            case "country":
                route = route.format(country_id="5")
            case "genre":
                route = route.format(genre_id="903")
            case "distributor":
                route = route.format(distributor_id="503")
            case "series":
                route = route.format(series_id="1")
            case "tag":
                route = route.format(tag="洋画")
            case "person":
                route = route.format(person_id="93709")
            case _:
                pass

        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") in {"Input should be less than or equal to 100", "Input should be less than or equal to 2000"}


@pytest.mark.parametrize("var", [
    "１",
    "abc123",
])
def test_list_path_vars_not_valid_integer(var) -> None:
    for type, route in list_routes.items():
        match type:
            case "award":
                route = route.format(award_id=var)
            case "year_series":
                route = route.format(year_series=var)
            case "year_specific":
                route = route.format(year=var)
            case "country":
                route = route.format(country_id=var)
            case "genre":
                route = route.format(genre_id=var)
            case "distributor":
                route = route.format(distributor_id=var)
            case "series":
                route = route.format(series_id=var)
            case "person":
                route = route.format(person_id=var)
            case _:
                continue

        resp = client.get(f"{route}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


def test_list_minimum_fields_present() -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "award":
                route = route.format(award_id="19")
            case "year_series":
                route = route.format(year_series="2010")
            case "year_specific":
                route = route.format(year="2001")
            case "country":
                route = route.format(country_id="5")
            case "genre":
                route = route.format(genre_id="903")
            case "distributor":
                route = route.format(distributor_id="503")
            case "series":
                route = route.format(series_id="1")
            case "tag":
                route = route.format(tag="洋画")
            case "person":
                route = route.format(person_id="93709")
            case _:
                pass

        resp = client.get(f"{route}?limit=5")
        resp_data = resp.json()

        assert resp.status_code == 200
        for movie in get_json_val(resp_data, "$.results.movies"):
            assert get_json_val(movie, "$.title") is not None
            assert get_json_val(movie, "$.rating") is not None
            assert get_json_val(movie, "$.mark_count") is not None
            assert get_json_val(movie, "$.clip_count") is not None
            assert get_json_val(movie, "$.movie_id") is not None
            assert get_json_val(movie, "$.link") is not None


def test_list_vod_all_minimum_fields_present() -> None:
    with open(file="tests/movie/movie_vod_name.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for vod_name in test_data:
        resp = client.get(f"{list_routes["vod"].format(vod_name=vod_name)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.results.movies[0].title") is not None
        assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
        assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
        assert get_json_val(resp_data, "$.results.movies[0].link") is not None


@pytest.mark.parametrize("award_id", [
    "1",
    "19",
])
def test_list_award_all_minimum_fields_present(award_id) -> None:
    resp = client.get(f"{list_routes["award"].format(award_id=award_id)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.results.movies[0].title") is not None
    assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
    assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
    assert get_json_val(resp_data, "$.results.movies[0].link") is not None


def test_list_year_series_all_minimum_fields_present() -> None:
    with open(file="tests/movie/movie_year_series.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for year in test_data:
        resp = client.get(f"{list_routes["year_series"].format(year_series=year)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(year)
        assert get_json_val(resp_data, "$.results.movies[0].title") is not None
        assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
        assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
        assert get_json_val(resp_data, "$.results.movies[0].link") is not None


def test_list_year_specific_all_minimum_fields_present() -> None:
    with open(file="tests/movie/movie_year_specific.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for year in test_data:
        resp = client.get(f"{list_routes["year_specific"].format(year=year)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(year)
        assert get_json_val(resp_data, "$.results.movies[0].title") is not None
        assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
        assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
        assert get_json_val(resp_data, "$.results.movies[0].link") is not None


def test_list_country_all_minimum_fields_present() -> None:
    with open(file="tests/movie/movie_country_id.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)

    for country in test_data:
        country_name = get_json_val(country, "$.jp")
        country_id = get_json_val(country, "$.id")

        resp = client.get(f"{list_routes["country"].format(country_id=country_id)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(country_name)
        assert get_json_val(resp_data, "$.results.movies[0].title") is not None
        assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
        assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
        assert get_json_val(resp_data, "$.results.movies[0].link") is not None


@pytest.mark.parametrize("genre_id", [
    "17",
    "903",
])
def test_list_genre_all_minimum_fields_present(genre_id) -> None:
    resp = client.get(f"{list_routes["genre"].format(genre_id=genre_id)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.results.movies[0].title") is not None
    assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
    assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
    assert get_json_val(resp_data, "$.results.movies[0].link") is not None


@pytest.mark.parametrize("distributor_id", [
    "502",
    "503",
])
def test_list_distributor_all_minimum_fields_present(distributor_id) -> None:
    resp = client.get(f"{list_routes["distributor"].format(distributor_id=distributor_id)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.results.movies[0].title") is not None
    assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
    assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
    assert get_json_val(resp_data, "$.results.movies[0].link") is not None


@pytest.mark.parametrize("series_id", [
    "1",
    "76",
])
def test_list_series_all_minimum_fields_present(series_id) -> None:
    resp = client.get(f"{list_routes["series"].format(series_id=series_id)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.results.movies[0].title") is not None
    assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
    assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
    assert get_json_val(resp_data, "$.results.movies[0].link") is not None


@pytest.mark.parametrize("tag", [
    "洋画",
    "邦画",
])
def test_list_tag_all_minimum_fields_present(tag) -> None:
    resp = client.get(f"{list_routes["tag"].format(tag=tag)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.heading").startswith(f"#{tag}")
    assert get_json_val(resp_data, "$.results.movies[0].title") is not None
    assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
    assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
    assert get_json_val(resp_data, "$.results.movies[0].link") is not None


@pytest.mark.parametrize("person_id", [
    "25185",
    "169314"
])
def test_list_person_all_minimum_fields_present(person_id) -> None:
    resp = client.get(f"{list_routes["person"].format(person_id=person_id)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.results.movies[0].title") is not None
    assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
    assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].movie_id") is not None
    assert get_json_val(resp_data, "$.results.movies[0].link") is not None
