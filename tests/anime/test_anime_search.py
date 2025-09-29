from random import choice
from tests.test_utils import client, get_json_val, ANIME_JPN, ANIME_ENG
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
    "?q=ポケモンす&limit=a",
    "?q=デジモン&page=z",
    "?q=名探偵コナン&limit=@&page=1",
])
def test_search_input_not_valid_integer(query) -> None:
    resp = client.get(f"/search/animes{query}")
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
    resp = client.get(f"/search/animes{query}")
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
    resp = client.get(f"/search/animes{query}")
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
    resp = client.get(f"/search/animes{query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == ""
    assert get_json_val(resp_data, "$.heading") == ""
    assert ANIME_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.animes")) == 0


def test_search_without_results_page_1(caplog) -> None:
    query = '".*&^'
    resp = client.get(f"/search/animes?q={query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == '".*'
    assert get_json_val(resp_data, "$.heading").startswith('".*')
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.animes")) == 0


def test_search_without_results_page_2(caplog) -> None:
    query = "俺物語!!"  # page 1 returns results, refer to 'test_search_with_results_single'
    resp = client.get(f"/search/animes?q={query}&page=2")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.animes")) == 0


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "俺物語!!",
            "rating": 3.9,
            "mark_count": 5418,
            "clip_count": 1051,
            "series_id": 603,
            "season_id": 1373,
            "link": "https://filmarks.com/animes/603/1373",
            "release_date": "2015年04月08日",
            "playback_time": "23分",
            "production_company": ["マッドハウス"],
            "director": ["浅香守生"],
            "series_composer": ["高橋ナツコ"],
            "cast": ["江口拓也", "潘めぐみ"],
        },
    ],
)
def test_search_with_results_single(test_data, caplog) -> None:
    query = "俺物語!!"
    resp = client.get(f"/search/animes?q={query}&limit=1")
    resp_data = resp.json()
    animes = get_json_val(resp_data, "$.results.animes")

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text
    assert len(animes) == 1

    fields = [
        "title",
        "series_id",
        "season_id",
        "link",
        "release_date",
        "playback_time",
        "production_company",
        "director",
        "series_composer",
        "cast",
    ]
    for field in fields:
        assert get_json_val(animes[0], f"$.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(animes[0], "$.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(animes[0], "$.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(animes[0], "$.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(animes[0], "$.poster") is not None
    assert get_json_val(animes[0], "$.producer") is None
    assert get_json_val(animes[0], "$.executive_producer") is None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "のだめカンタービレ",
            "series_id": 1342,
            "season_id": 1783,
            "link": "https://filmarks.com/animes/1342/1783",
            "release_date": "2007年01月11日",
            "director": ["カサヰケンイチ"],
            "series_composer": ["金春智子"],
            "cast": ["川澄綾子", "関智一"],
        },
        {
            "title": "のだめカンタービレ 巴里編",
            "series_id": 1342,
            "season_id": 1784,
            "link": "https://filmarks.com/animes/1342/1784",
            "release_date": "2008年10月09日",
            "director": ["今千秋"],
            "series_composer": ["榎戸洋司"],
            "cast": ["川澄綾子", "関智一"],
        },
        {
            "title": "のだめカンタービレ フィナーレ",
            "series_id": 1342,
            "season_id": 1785,
            "link": "https://filmarks.com/animes/1342/1785",
            "release_date": "2010年01月14日",
            "director": ["今千秋"],
            "series_composer": ["中島かずき"],
            "cast": ["川澄綾子", "関智一"],
        },
    ],
)
def test_search_with_results_multiple(test_data, caplog) -> None:
    query = "のだめカンタービレ"
    resp = client.get(f"/search/animes?q={query}&page=1")
    resp_data = resp.json()
    anime = next(a for a in get_json_val(resp_data, "$.results.animes") if get_json_val(a, "$.title") == get_json_val(test_data, "$.title"))

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text

    fields = [
        "title",
        "series_id",
        "season_id",
        "link",
        "release_date",
        "director",
        "series_composer",
        "cast",
    ]
    for field in fields:
        assert get_json_val(anime, f"$.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(anime, "$.rating") is not None
    assert get_json_val(anime, "$.mark_count") is not None
    assert get_json_val(anime, "$.clip_count") is not None
    assert get_json_val(anime, "$.poster") is not None
    assert get_json_val(anime, "$.producer") is None
    assert get_json_val(anime, "$.executive_producer") is None


def test_search_with_results_random(caplog) -> None:
    with open(file="tests/anime/100_animes.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        anime = choice(test_data)

    query = get_json_val(anime, "$.title")
    series_id = get_json_val(anime, "$.series")
    season_id = get_json_val(anime, "$.season")

    resp = client.get(f"/search/animes?q={query}&limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert ANIME_JPN in get_json_val(resp_data, "$.heading")
    assert ANIME_ENG in caplog.text

    assert get_json_val(resp_data, "$.results.animes[0].title") == query
    assert get_json_val(resp_data, "$.results.animes[0].rating") is not None
    assert get_json_val(resp_data, "$.results.animes[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.animes[0].series_id") == series_id
    assert get_json_val(resp_data, "$.results.animes[0].season_id") == season_id
    assert get_json_val(resp_data, "$.results.animes[0].link") is not None
