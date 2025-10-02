from tests.conftest import get_json_val, ANIME_JPN, ANIME_ENG
import pytest

list_routes = {
    "trend": "/list-anime/trend",
    "vod": "/list-anime/vod/{vod_name}",
    "year_series": "/list-anime/year/{year_series}s",
    "year_specific": "/list-anime/year/{year}",
    "year_season": "/list-anime/year/{year}/{season_id}",
    "company": "/list-anime/company/{company_id}",
    "tag": "/list-anime/tag/{tag}",
    "person": "/list-anime/person/{person_id}",
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
def test_list_query_params_not_valid_integer(client_nc, query) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "year_season":
                route = route.format(year="2019", season_id="1")
            case "company":
                route = route.format(company_id="41")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="274563")
            case _:
                pass

        resp = client_nc.get(f"{route}{query}")
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
def test_list_query_params_less_than_min_threshold(client_nc, query) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "year_season":
                route = route.format(year="2019", season_id="1")
            case "company":
                route = route.format(company_id="41")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="274563")
            case _:
                pass

        resp = client_nc.get(f"{route}{query}")
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
def test_list_query_params_more_than_max_threshold(client_nc, query) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "year_season":
                route = route.format(year="2019", season_id="1")
            case "company":
                route = route.format(company_id="41")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="274563")
            case _:
                pass

        resp = client_nc.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") in {"Input should be less than or equal to 100", "Input should be less than or equal to 10000"}


@pytest.mark.parametrize("var", [
    "１",
    "abc123",
])
def test_list_path_vars_not_valid_integer(client_nc, var) -> None:
    for type, route in list_routes.items():
        match type:
            case "year_series":
                route = route.format(year_series=var)
            case "year_specific":
                route = route.format(year=var)
            case "year_season":
                route = route.format(year="2019", season_id=var)
            case "company":
                route = route.format(company_id=var)
            case "person":
                route = route.format(person_id=var)
            case _:
                continue

        resp = client_nc.get(f"{route}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


def test_list_minimum_fields_present(client_nc, caplog) -> None:
    for type, route in list_routes.items():
        match type:
            case "vod":
                route = route.format(vod_name="prime_video")
            case "year_series":
                route = route.format(year_series="2020")
            case "year_specific":
                route = route.format(year="2019")
            case "year_season":
                route = route.format(year="2019", season_id="1")
            case "company":
                route = route.format(company_id="41")
            case "tag":
                route = route.format(tag="神作")
            case "person":
                route = route.format(person_id="274563")
            case _:
                pass

        resp = client_nc.get(f"{route}?limit=5")
        resp_data = resp.json()

        assert resp.status_code == 200
        for anime in get_json_val(resp_data, "$.results.animes"):
            assert ANIME_JPN in get_json_val(resp_data, "$.heading")
            assert ANIME_ENG in caplog.text
            assert get_json_val(anime, "$.title") is not None
            assert get_json_val(anime, "$.rating") is not None
            assert get_json_val(anime, "$.mark_count") is not None
            assert get_json_val(anime, "$.clip_count") is not None
            assert get_json_val(anime, "$.series_id") is not None
            assert get_json_val(anime, "$.season_id") is not None
            assert get_json_val(anime, "$.link") is not None


def test_list_vod_all_minimum_fields_present(client_nc, caplog) -> None:
    with open(file="tests/anime/anime_vod_name.txt", mode="r", encoding="utf-8") as f:
        test_data = (tuple(line.strip().split(",")) for line in f.readlines())

    for vod_name, vod_title in test_data:
        resp = client_nc.get(f"{list_routes["vod"].format(vod_name=vod_name)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(vod_title)
        assert ANIME_JPN in get_json_val(resp_data, "$.heading")
        assert ANIME_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.animes[0].title") is not None
        assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
        assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].link") is not None


def test_list_year_series_all_minimum_fields_present(client_nc, caplog) -> None:
    with open(file="tests/anime/anime_year_series.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for year in test_data:
        resp = client_nc.get(f"{list_routes["year_series"].format(year_series=year)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(f"{year}年代")
        assert ANIME_JPN in get_json_val(resp_data, "$.heading")
        assert ANIME_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.animes[0].title") is not None
        assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
        assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].link") is not None


def test_list_year_specific_all_minimum_fields_present(client_nc, caplog) -> None:
    with open(file="tests/anime/anime_year_specific.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for year in test_data:
        resp = client_nc.get(f"{list_routes["year_specific"].format(year=year)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(f"{year}年")
        assert ANIME_JPN in get_json_val(resp_data, "$.heading")
        assert ANIME_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.animes[0].title") is not None
        assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
        assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].link") is not None


def test_list_year_season_all_minimum_fields_present(client_nc, caplog) -> None:
    with open(file="tests/anime/anime_year_season.txt", mode="r", encoding="utf-8") as f:
        test_data = (tuple(line.strip().split(",")) for line in f.readlines())

    for year, season_id in test_data:
        resp = client_nc.get(f"{list_routes["year_season"].format(year=year, season_id=season_id)}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(f"{year}年")
        assert "冬" if season_id == "1" else "春" if season_id == "4" else "夏" if season_id == "7" else "秋" in get_json_val(resp_data, "$.heading")
        assert ANIME_JPN in get_json_val(resp_data, "$.heading")
        assert ANIME_ENG in caplog.text
        assert get_json_val(resp_data, "$.results.animes[0].title") is not None
        assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
        assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.animes[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.animes[0].link") is not None


@pytest.mark.parametrize("company", [
    ("1", "J.C.STAFF"),
    ("3", "京都アニメーション"),
    ("41", "東映アニメーション")
])
def test_list_company_all_minimum_fields_present(client_nc, company, caplog) -> None:
    resp = client_nc.get(f"{list_routes["company"].format(company_id=company[0])}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.heading").startswith(f"{company[1]}")
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text
    assert get_json_val(resp_data, "$.results.animes[0].title") is not None
    assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
    assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].series_id") is not None
    assert get_json_val(resp_data, "$.results.animes[0].season_id") is not None
    assert get_json_val(resp_data, "$.results.animes[0].link") is not None


@pytest.mark.parametrize("tag", [
    "駄作",
    "神作",
    "平成ヒット",
    "令和ヒット",
    "漫画原作",
])
def test_list_tag_all_minimum_fields_present(client_nc, tag, caplog) -> None:
    resp = client_nc.get(f"{list_routes["tag"].format(tag=tag)}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.heading").startswith(f"#{tag}")
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text
    assert get_json_val(resp_data, "$.results.animes[0].title") is not None
    assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
    assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].series_id") is not None
    assert get_json_val(resp_data, "$.results.animes[0].season_id") is not None
    assert get_json_val(resp_data, "$.results.animes[0].link") is not None


@pytest.mark.parametrize("person", [
    ("25499", "満島ひかり"),
    ("240371", "鬼頭明里"),
    ("274563", "前田愛")
])
def test_list_person_all_minimum_fields_present(client_nc, person, caplog) -> None:
    resp = client_nc.get(f"{list_routes["person"].format(person_id=person[0])}?limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.heading").startswith(f"{person[1]}")
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text
    assert get_json_val(resp_data, "$.results.animes[0].title") is not None
    assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
    assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].series_id") is not None
    assert get_json_val(resp_data, "$.results.animes[0].season_id") is not None
    assert get_json_val(resp_data, "$.results.animes[0].link") is not None
