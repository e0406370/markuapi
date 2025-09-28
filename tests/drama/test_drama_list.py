from tests.test_utils import client, get_json_val, DRAMA_JPN, DRAMA_ENG
import json
import pytest

list_routes = {
    "trend": "/list-drama/trend",
    "vod": "/list-drama/vod/{vod_name}",
    "year_series": "/list-drama/year/{year_series}s",
    "year_specific": "/list-drama/year/{year}",
    "country": "/list-drama/country/{country_id}",
    "genre": "/list-drama/genre/{genre_id}",
    "tag": "/list-drama/tag/{tag}",
    "person": "/list-drama/person/{person_id}",
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
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "country":
                route = route.format(country_id="144")
            case "genre":
                route = route.format(genre_id="7")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="25499")
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
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "country":
                route = route.format(country_id="144")
            case "genre":
                route = route.format(genre_id="7")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="25499")
            case _:
                pass

        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be greater than 0"


@pytest.mark.parametrize("query", [
    "?limit=101",
    "?page=10001",
    "?limit=101&page=3",
    "?limit=100&page=10001",
])
def test_list_query_params_more_than_max_threshold(query) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "country":
                route = route.format(country_id="144")
            case "genre":
                route = route.format(genre_id="7")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="25499")
            case _:
                pass

        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") in {"Input should be less than or equal to 100", "Input should be less than or equal to 10000"}


@pytest.mark.parametrize("var", [
    "１",
    "abc123",
])
def test_list_path_vars_not_valid_integer(var) -> None:
    for type, route in list_routes.items():
        match type:
            case "year_series":
                route = route.format(year_series=var)
            case "year_specific":
                route = route.format(year=var)
            case "country":
                route = route.format(country_id=var)
            case "genre":
                route = route.format(genre_id=var)
            case "person":
                route = route.format(person_id=var)
            case _:
                continue

        resp = client.get(f"{route}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


def test_list_minimum_fields_present(caplog) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "country":
                route = route.format(country_id="144")
            case "genre":
                route = route.format(genre_id="7")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="25499")
            case _:
                pass

        resp = client.get(f"{route}?limit=5")
        resp_data = resp.json()

        assert resp.status_code == 200
        for drama in get_json_val(resp_data, "$.results.dramas"):
            assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
            assert DRAMA_ENG in caplog.text
            assert get_json_val(drama, "$.title") is not None
            assert get_json_val(drama, "$.rating") is not None
            assert get_json_val(drama, "$.mark_count") is not None
            assert get_json_val(drama, "$.clip_count") is not None
            assert get_json_val(drama, "$.series_id") is not None
            assert get_json_val(drama, "$.season_id") is not None
            assert get_json_val(drama, "$.link") is not None


def test_list_vod_all_minimum_fields_present(caplog) -> None:
    with open(file="tests/drama/drama_vod_name.txt", mode="r", encoding="utf-8") as f:
        test_data = (tuple(line.strip().split(",")) for line in f.readlines())

    for vod_name, vod_title in test_data:
        resp = client.get(f"{list_routes["vod"].format(vod_name=vod_name)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(vod_title)
        assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
        assert DRAMA_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].link") is not None


def test_list_year_series_all_minimum_fields_present(caplog) -> None:
    with open(file="tests/drama/drama_year_series.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for year in test_data:
        resp = client.get(f"{list_routes["year_series"].format(year_series=year)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(f"{year}年代")
        assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
        assert DRAMA_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].link") is not None


def test_list_year_specific_all_minimum_fields_present(caplog) -> None:
    with open(file="tests/drama/drama_year_specific.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for year in test_data:
        resp = client.get(f"{list_routes["year_specific"].format(year=year)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(f"{year}年")
        assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
        assert DRAMA_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].link") is not None


def test_list_country_all_minimum_fields_present(caplog) -> None:
    with open(file="tests/drama/drama_country_id.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)

    for country in test_data:
        country_name = get_json_val(country, "$.jp")
        country_id = get_json_val(country, "$.id")

        resp = client.get(f"{list_routes["country"].format(country_id=country_id)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(country_name)
        assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
        assert DRAMA_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].link") is not None


def test_list_genre_all_minimum_fields_present(caplog) -> None:
    with open(file="tests/drama/drama_genre_id.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)

    for genre in test_data:
        genre_name = get_json_val(genre, "$.jp")
        genre_id = get_json_val(genre, "$.id")

        resp = client.get(f"{list_routes["genre"].format(genre_id=genre_id)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(genre_name)
        assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
        assert DRAMA_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].link") is not None


@pytest.mark.parametrize("tag", [
    "駄作",
    "神作",
    "平成ヒット",
    "令和ヒット",
    "漫画原作",
    "1話30分以内",
])
def test_list_tag_all_minimum_fields_present(tag, caplog) -> None:
    resp = client.get(f"{list_routes["tag"].format(tag=tag)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.heading").startswith(f"#{tag}")
    assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
    assert DRAMA_ENG in caplog.text
    assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].link") is not None


@pytest.mark.parametrize("person", [
    ("25499", "満島ひかり"),
    ("79213", "山﨑賢人"),
    ("125964", "戸田恵梨香")
])
def test_list_person_all_minimum_fields_present(person, caplog) -> None:
    resp = client.get(f"{list_routes["person"].format(person_id=person[0])}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.heading").startswith(f"{person[1]}")
    assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
    assert DRAMA_ENG in caplog.text
    assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].link") is not None
