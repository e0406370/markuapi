from random import choice
from tests.conftest import get_json_val, MOVIE_JPN, MOVIE_ENG
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
    "?q=ハリーポッター&limit=a",
    "?q=ちはやふる&page=z",
    "?q=ラストマイル&limit=@&page=1",
])
def test_search_input_not_valid_integer(client_nc, query) -> None:
    resp = client_nc.get(f"/search/movies{query}")
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
def test_search_input_less_than_min_threshold(client_nc, query) -> None:
    resp = client_nc.get(f"/search/movies{query}")
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
def test_search_input_more_than_max_threshold(client_nc, query) -> None:
    resp = client_nc.get(f"/search/movies{query}")
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
def test_search_empty_query(client_nc, query, caplog) -> None:
    resp = client_nc.get(f"/search/movies{query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == ""
    assert get_json_val(resp_data, "$.heading") == ""
    assert MOVIE_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.movies")) == 0


def test_search_without_results_page_1(client_nc, caplog) -> None:
    query = '".*&^'
    resp = client_nc.get(f"/search/movies?q={query}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == '".*'
    assert get_json_val(resp_data, "$.heading").startswith('".*')
    assert MOVIE_JPN in get_json_val(resp_data, "$.heading")
    assert MOVIE_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.movies")) == 0


def test_search_without_results_page_2(client_nc, caplog) -> None:
    query = "ちはやふる"  # page 1 returns results, refer to 'test_search_with_results_multiple'
    resp = client_nc.get(f"/search/movies?q={query}&page=2")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert MOVIE_JPN in get_json_val(resp_data, "$.heading")
    assert MOVIE_ENG in caplog.text
    assert len(get_json_val(resp_data, "$.results.movies")) == 0


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "プラダを着た悪魔",
            "rating": 4.1,
            "mark_count": 378397,
            "clip_count": 89715,
            "movie_id": 2151,
            "link": "https://filmarks.com/movies/2151",
            "screening_date": "2006年11月18日",
            "screening_time": "110分",
            "country_of_origin": ["アメリカ"],
            "genre": ["ドラマ", "恋愛", "コメディ"],
            "distributor": ["20世紀フォックス映画"],
            "director": ["デヴィッド・フランケル"],
            "scriptwriter": ["アライン・ブロッシュ・マッケンナ"],
            "cast": ["メリル・ストリープ", "アン・ハサウェイ"],
        },
    ],
)
def test_search_with_results_single(client_nc, test_data, caplog) -> None:
    query = "プラダを着た悪魔"
    resp = client_nc.get(f"/search/movies?q={query}&limit=1")
    resp_data = resp.json()
    movies = get_json_val(resp_data, "$.results.movies")

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert MOVIE_JPN in get_json_val(resp_data, "$.heading")
    assert MOVIE_ENG in caplog.text
    assert len(movies) == 1

    fields = [
        "title",
        "movie_id",
        "link",
        "screening_date",
        "screening_time",
        "country_of_origin",
        "genre",
        "distributor",
        "director",
        "scriptwriter",
        "cast",
    ]
    for field in fields:
        assert get_json_val(movies[0], f"$.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(movies[0], "$.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(movies[0], "$.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(movies[0], "$.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(movies[0], "$.poster") is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "ちはやふる 上の句",
            "movie_id": 62655,
            "link": "https://filmarks.com/movies/62655",
            "screening_date": "2016年03月19日",
            "screening_time": "111分",
            "country_of_origin": ["日本"],
            "director": ["小泉徳宏"],
            "cast": ["広瀬すず", "野村周平"],
        },
        {
            "title": "ちはやふる 下の句",
            "movie_id": 62920,
            "link": "https://filmarks.com/movies/62920",
            "screening_date": "2016年04月29日",
            "screening_time": "103分",
            "country_of_origin": ["日本"],
            "director": ["小泉徳宏"],
            "cast": ["広瀬すず", "野村周平", "新田真剣佑"],
        },
        {
            "title": "ちはやふる ー結びー",
            "movie_id": 73729,
            "link": "https://filmarks.com/movies/73729",
            "screening_date": "2018年03月17日",
            "screening_time": "128分",
            "country_of_origin": ["日本"],
            "director": ["小泉徳宏"],
            "cast": ["広瀬すず", "野村周平"],
        },
    ],
)
def test_search_with_results_multiple(client_nc, test_data, caplog) -> None:
    query = "ちはやふる"
    resp = client_nc.get(f"/search/movies?q={query}&page=1&limit=3")
    resp_data = resp.json()
    movie = next(m for m in get_json_val(resp_data, "$.results.movies") if get_json_val(m, "$.title") == get_json_val(test_data, "$.title"))

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert MOVIE_JPN in get_json_val(resp_data, "$.heading")
    assert MOVIE_ENG in caplog.text

    fields = [
        "title",
        "movie_id",
        "link",
        "screening_date",
        "screening_time",
        "country_of_origin",
        "director",
        "cast",
    ]
    for field in fields:
        assert get_json_val(movie, f"$.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(movie, "$.rating") is not None
    assert get_json_val(movie, "$.mark_count") is not None
    assert get_json_val(movie, "$.clip_count") is not None
    assert get_json_val(movie, "$.poster") is not None
    assert get_json_val(movie, "$.genre") is not None
    assert get_json_val(movie, "$.distributor") is not None


def test_search_with_results_random(client_nc, caplog) -> None:
    with open(file="tests/movie/100_movies.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        movie = choice(test_data)

    query = get_json_val(movie, "$.title")
    movie_id = get_json_val(movie, "$.id")

    resp = client_nc.get(f"/search/movies?q={query}&limit=1")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.query") == query
    assert get_json_val(resp_data, "$.heading").startswith(query)
    assert MOVIE_JPN in get_json_val(resp_data, "$.heading")
    assert MOVIE_ENG in caplog.text

    assert get_json_val(resp_data, "$.results.movies[0].title") == query
    assert get_json_val(resp_data, "$.results.movies[0].rating") is not None
    assert get_json_val(resp_data, "$.results.movies[0].mark_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].clip_count") is not None
    assert get_json_val(resp_data, "$.results.movies[0].movie_id") == movie_id
    assert get_json_val(resp_data, "$.results.movies[0].link") is not None
