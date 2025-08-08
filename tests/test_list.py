from tests.test_utils import client, get_json_val
import pytest

list_routes = [
    "/list-drama/trend",
    "/list-drama/country/144",
    "/list-drama/year/2019",
]


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
def test_list_input_not_valid_integer(query) -> None:
    for route in list_routes:
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
def test_list_input_less_than_min_threshold(query) -> None:
    for route in list_routes:
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
def test_list_input_more_than_max_threshold(query) -> None:
    for route in list_routes:
        resp = client.get(f"{route}{query}")
        resp_data = resp.json()

        assert resp.status_code == 422
        for err in get_json_val(resp_data, "$.detail"):
            assert get_json_val(err, "$.msg") == "Input should be less than or equal to 1000"


def test_list_minimum_fields_present() -> None:
    for route in list_routes:    
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
