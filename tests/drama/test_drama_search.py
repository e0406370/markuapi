from random import choice
from tests.test_utils import client, get_json_val, DRAMA_JPN, DRAMA_ENG
import json
import pytest


@pytest.mark.parametrize("query", [
    "?limit",
    "?limit=", 
    "?limit=abc123",
    "?limit=１",
    "?page",
    "?page=", 
    "?page=def456",
    "?page=２",
    "?q=あなたの番です&limit=a",
    "?q=ちはやふる&page=z",
    "?q=コンフィデンスマンJP&limit=@&page=1",
])
def test_search_input_not_valid_integer(query) -> None:
    resp = client.get(f"/search/dramas{query}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize("query", [
    "?limit=-1",
    "?limit=0",
    "?page=-5", 
    "?page=0",
    "?q=test1&limit=-1",
    "?q=test2&page=-2",
    "?q=test3&limit=1&page=0",
])
def test_search_input_less_than_min_threshold(query) -> None:
    resp = client.get(f"/search/dramas{query}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be greater than 0"


@pytest.mark.parametrize("query", [
    "?limit=101",
    "?page=10001",
    "?q=test1&limit=101",
    "?q=test2&page=10001",
    "?q=test3&limit=101&page=3",
])
def test_search_input_more_than_max_threshold(query) -> None:
    resp = client.get(f"/search/dramas{query}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") in {"Input should be less than or equal to 100", "Input should be less than or equal to 10000"}


@pytest.mark.parametrize("query", [
    "",
    "?",
    "?q",
    "?q&page=2",
    "?q=",
    "?q=&limit=1",
])
def test_search_empty_query(query, caplog) -> None:
    resp = client.get(f"/search/dramas{query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == ""
    assert get_json_val(resp_data, "$.heading") == ""
    assert DRAMA_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.dramas")) == 0


def test_search_without_results_page_1(caplog) -> None:
    query = '".*&^'
    resp = client.get(f"/search/dramas?q={query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == '".*'
    assert get_json_val(resp_data, "$.heading").startswith('".*')
    assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
    assert DRAMA_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.dramas")) == 0


def test_search_without_results_page_2(caplog) -> None:
    query = "ちはやふる"  # page 1 returns results, refer to 'test_search_with_results_multiple'
    resp = client.get(f"/search/dramas?q={query}&page=2")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
    assert DRAMA_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.dramas")) == 0


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "あなたの番です",
            "rating": 4.0,
            "mark_count": 30697,
            "clip_count": 6178,
            "series_id": 6055,
            "season_id": 8586,
            "link": "https://filmarks.com/dramas/6055/8586",
            "release_date": "2019年04月14日",
            "playback_time": "46分",
            "country_of_origin": ["日本"],
            "genre": ["ミステリー"],
            "scriptwriter": ["福原充則"],
            "cast": ["原田知世", "田中圭", "西野七瀬"],
        },
    ],
)
def test_search_with_results_single(test_data, caplog) -> None:
    query = "あなたの番です"
    resp = client.get(f"/search/dramas?q={query}&limit=5")
    resp_data = resp.json()
    dramas = get_json_val(resp_data, "$.results.dramas")

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
    assert DRAMA_ENG in caplog.text
    assert len(dramas) == 5

    fields = [
        "title",
        "series_id",
        "season_id",
        "link",
        "release_date",
        "playback_time",
        "country_of_origin",
        "genre",
        "scriptwriter",
        "cast",
    ]
    for field in fields:
        assert get_json_val(dramas[0], f"$.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(dramas[0], "$.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(dramas[0], "$.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(dramas[0], "$.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(dramas[0], "$.poster") is not None
    assert get_json_val(dramas[0], "$.executive_producer") is None
    assert get_json_val(dramas[0], "$.director") is None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "ちはやふる－めぐり－",
            "series_id": 16234,
            "season_id": 21896,
            "link": "https://filmarks.com/dramas/16234/21896",
            "release_date": "2025年07月09日",
            "playback_time": "50分",
            "country_of_origin": ["日本"],
            "director": ["藤田直哉", "本田大介"],
            "cast": ["當真あみ", "上白石萌音"],
        },
        {
            "title": "ちはやふる ー繋ぐー",
            "series_id": 973,
            "season_id": 2117,
            "link": "https://filmarks.com/dramas/973/2117",
            "release_date": "2018年02月20日",
            "playback_time": "10分",
            "country_of_origin": ["日本"],
            "director": ["小泉徳宏"],
            "cast": ["広瀬すず", "野村周平", "新田真剣佑"],
        },
    ],
)
def test_search_with_results_multiple(test_data, caplog) -> None:
    query = "ちはやふる"
    resp = client.get(f"/search/dramas?q={query}&page=1")
    resp_data = resp.json()
    drama = next(d for d in get_json_val(resp_data, "$.results.dramas") if get_json_val(d, "$.title") == get_json_val(test_data, "$.title"))

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
    assert DRAMA_ENG in caplog.text

    fields = [
        "title",
        "series_id",
        "season_id",
        "link",
        "release_date",
        "playback_time",
        "country_of_origin",
        "director",
        "cast",
    ]
    for field in fields:
        assert get_json_val(drama, f"$.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(drama, "$.rating") is not None
    assert get_json_val(drama, "$.mark_count") is not None
    assert get_json_val(drama, "$.clip_count") is not None
    assert get_json_val(drama, "$.poster") is not None
    assert get_json_val(drama, "$.executive_producer") is None
    assert get_json_val(drama, "$.scriptwriter") is None


def test_search_with_results_random(caplog) -> None:
    with open(file="tests/drama/100_dramas.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        drama = choice(test_data)

    query = get_json_val(drama, "$.title")
    series_id = get_json_val(drama, "$.series")
    season_id = get_json_val(drama, "$.season")

    resp = client.get(f"/search/dramas?q={query}&limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert DRAMA_JPN in get_json_val(resp_data, "$.heading")
    assert DRAMA_ENG in caplog.text

    assert get_json_val(resp_data, "$.results.dramas[0].title") == query
    assert get_json_val(resp_data, "$.results.dramas[0].rating") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.dramas[0].series_id") == series_id
    assert get_json_val(resp_data, "$.results.dramas[0].season_id") == season_id
    assert get_json_val(resp_data, "$.results.dramas[0].link") is not None
