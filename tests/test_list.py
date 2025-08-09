from tests.test_utils import client, get_json_val
import json
import pytest

list_routes = {
    "trend": "/list-drama/trend",
    "country": "/list-drama/country",
    "year": "/list-drama/year",
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
            case "country":
                route += "/144"
            case "year":
                route += "/2019"
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
            case "country":
                route += "/144"
            case "year":
                route += "/2019"
            case _:
                pass

        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be greater than 0"


@pytest.mark.parametrize("query", [
    "?limit=1001",
    "?page=2000",
    "?limit=1001&page=3",
    "?limit=1000&page=1001",
])
def test_list_query_params_more_than_max_threshold(query) -> None:
    for type, route in list_routes.items():
        match type:
            case "country":
                route += "/144"
            case "year":
                route += "/2019"
            case _:
                pass

        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be less than or equal to 1000"


def test_list_minimum_fields_present() -> None:
    for type, route in list_routes.items():
        match type:
            case "country":
                route += "/144"
            case "year":
                route += "/2019"
            case _:
                pass

        resp = client.get(f"{route}?limit=5")
        resp_data = resp.json()

        assert resp.status_code == 200
        for drama in get_json_val(resp_data, "$.results.dramas"):
            assert get_json_val(drama, "$.title") is not None
            assert get_json_val(drama, "$.rating") is not None
            assert get_json_val(drama, "$.mark_count") is not None
            assert get_json_val(drama, "$.clip_count") is not None
            assert get_json_val(drama, "$.series_id") is not None
            assert get_json_val(drama, "$.season_id") is not None
            assert get_json_val(drama, "$.link") is not None


@pytest.mark.parametrize("var", [
    "１４４",
    "abc123",
])
def test_list_country_id_not_valid_integer(var) -> None:
    resp = client.get(f"{list_routes["country"]}/{var}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


def test_list_country_all_minimum_fields_present() -> None:
    with open(file="tests/___country_id.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)

    for country in test_data:
        country_name = get_json_val(country, "$.jp")
        country_id = get_json_val(country, "$.id")

        resp = client.get(f"{list_routes["country"]}/{country_id}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(country_name)
        assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].link") is not None


@pytest.mark.parametrize("var", [
    "２０１９",
    "xyz987",
])
def test_list_year_id_not_valid_integer(var) -> None:
    resp = client.get(f"{list_routes["year"]}/{var}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


def test_list_year_all_minimum_fields_present() -> None:
    with open(file="tests/___year_id.txt", mode="r", encoding="utf-8") as f:
        test_data = (line.strip() for line in f.readlines())

    for year in test_data:
        resp = client.get(f"{list_routes["year"]}/{year}?limit=1")
        resp_data = resp.json()

        assert resp.status_code == 200
        assert get_json_val(resp_data, "$.heading").startswith(year)
        assert get_json_val(resp_data, "$.results.dramas[0].title") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].series_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].season_id") is not None
        assert get_json_val(resp_data, "$.results.dramas[0].link") is not None
