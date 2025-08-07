from random import choice
from tests.test_utils import client, get_json_val
import json
import pytest


@pytest.mark.parametrize("path", [
    "abc/xyz",
    "6055/t",
    "hi/8586",
    "８０４２/11683",
    "8042/１１６８３"
])
def test_info_input_not_valid_integer(path) -> None:
    resp = client.get(f"/dramas/{path}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "魔女ユヒ",
            "original_title": "마녀유희",
            "rating": 3.5,
            "mark_count": 48,
            "clip_count": 13,
            "series_id": 11358,
            "season_id": 15763,
            "link": "https://filmarks.com/dramas/11358/15763",
            "production_year_series": "https://filmarks.com/list-drama/year/2000s/2007",
            "production_year": "2007年",
            "country_of_origin": "韓国",
            "cast": [
                {
                    "name": "ハン・ガイン",
                    "character": "マ･ユヒ",
                    "people_id": 175097,
                    "link": "https://filmarks.com/people/175097",
                },
                {
                    "name": "ジェヒ",
                    "character": "チェ･ムリョン",
                    "people_id": 4988,
                    "link": "https://filmarks.com/people/4988",
                },
                {
                    "name": "キム・ジョンフン",
                    "character": "ユ･ジュナ",
                    "people_id": 91733,
                    "link": "https://filmarks.com/people/91733",
                },
                {
                    "name": "チョン・ヘビン",
                    "character": "ナム･スンミ",
                    "people_id": 74428,
                    "link": "https://filmarks.com/people/74428",
                },
                {
                    "name": "ピョン・ヒボン",
                    "character": "マ会長",
                    "people_id": 50683,
                    "link": "https://filmarks.com/people/50683",
                },
                {
                    "name": "アン・ソクファン",
                    "character": "チェ･ビョンソ",
                    "people_id": 185994,
                    "link": "https://filmarks.com/people/185994",
                },
                {
                    "name": "イ・チェヨン",
                    "people_id": 194890,
                    "link": "https://filmarks.com/people/194890",
                },
                {
                    "name": "ソン・ドンイル",
                    "character": "イ･チーフ",
                    "people_id": 176298,
                    "link": "https://filmarks.com/people/176298",
                },
                {
                    "name": "パク・ボヨン",
                    "people_id": 85588,
                    "link": "https://filmarks.com/people/85588",
                }
            ],
        },
    ],
)
def test_info_with_results_single(test_data) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")
    resp = client.get(f"/dramas/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.series_id") == series_id
    assert get_json_val(resp_data, "$.season_id") == season_id

    fields = [
        "title",
        "original_title",
        "link",
        "production_year_series",
        "production_year",
        "country_of_origin",
        "cast",
    ]
    for field in fields:
      assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") == pytest.approx(get_json_val(test_data, "$.mark_count"), abs=500)
    assert get_json_val(resp_data, "$.data.clip_count") == pytest.approx(get_json_val(test_data, "$.clip_count"), abs=500)

    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.release_date") is None
    assert get_json_val(resp_data, "$.data.playback_time") is None
    assert get_json_val(resp_data, "$.data.synopsis") is None
    assert get_json_val(resp_data, "$.data.genre") is None
    assert get_json_val(resp_data, "$.data.creator") is None
    assert get_json_val(resp_data, "$.data.director") is None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is None


def test_info_with_results_random() -> None:
    with open(file="tests/__100_dramas.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        drama = choice(test_data)

    series_id = get_json_val(drama, "$.series")
    season_id = get_json_val(drama, "$.season")
    resp = client.get(f"/dramas/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.series_id") == series_id
    assert get_json_val(resp_data, "$.season_id") == season_id

    assert get_json_val(resp_data, "$.data.title") is not None
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.mark_count") is not None
    assert get_json_val(resp_data, "$.data.clip_count") is not None
    assert get_json_val(resp_data, "$.data.link") is not None
    assert get_json_val(resp_data, "$.data.production_year_series") is not None
    assert get_json_val(resp_data, "$.data.production_year") is not None
