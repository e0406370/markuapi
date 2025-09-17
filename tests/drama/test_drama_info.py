from random import choice
from tests.test_utils import client, get_json_val
import json
import pytest


@pytest.mark.parametrize("path", [
    "abc/xyz",
    "6055/t",
    "hi/8586",
    "８０４２/11683",
    "8042/１１６８３",
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
            "title": "コード・ブルー ドクターヘリ緊急救命 1st season",
            "rating": 4.2,
            "mark_count": 17116,
            "clip_count": 2716,
            "series_id": 1137,
            "season_id": 2418,
            "link": "https://filmarks.com/dramas/1137/2418",
            "production_year_link": "https://filmarks.com/list-drama/year/2000s/2008",
            "production_year": 2008,
            "release_date": "2008年07月03日",
            "playback_time": "47分",
            "country_of_origin": [
                {
                    "name": "日本",
                    "id": 144,
                    "link": "https://filmarks.com/list-drama/country/144",
                }
            ],
            "cast": [
                {
                    "name": "山下智久",
                    "character": "藍沢 耕作",
                    "id": 182202,
                    "link": "https://filmarks.com/people/182202",
                },
                {
                    "name": "新垣結衣",
                    "character": "白石 恵",
                    "id": 95311,
                    "link": "https://filmarks.com/people/95311",
                },
                {
                    "name": "戸田恵梨香",
                    "character": "緋山 美帆子",
                    "id": 125964,
                    "link": "https://filmarks.com/people/125964",
                },
                {
                    "name": "比嘉愛未",
                    "character": "冴島 はるか",
                    "id": 123887,
                    "link": "https://filmarks.com/people/123887",
                },
                {
                    "name": "浅利陽介",
                    "character": "藤川 一男",
                    "id": 57612,
                    "link": "https://filmarks.com/people/57612",
                },
                {
                    "name": "児玉清",
                    "character": "田所 良昭",
                    "id": 35808,
                    "link": "https://filmarks.com/people/35808",
                },
                {
                    "name": "勝村政信",
                    "character": "森本 忠士",
                    "id": 178763,
                    "link": "https://filmarks.com/people/178763",
                },
                {
                    "name": "寺島進",
                    "character": "梶 寿志",
                    "id": 67642,
                    "link": "https://filmarks.com/people/67642",
                },
                {
                    "name": "杉本哲太",
                    "character": "西条 章",
                    "id": 537,
                    "link": "https://filmarks.com/people/537",
                },
                {
                    "name": "りょう",
                    "character": "三井 環奈",
                    "id": 179914,
                    "link": "https://filmarks.com/people/179914",
                },
                {
                    "name": "柳葉敏郎",
                    "character": "黒田 脩二",
                    "id": 146784,
                    "link": "https://filmarks.com/people/146784",
                },
            ],
        },
    ],
)
def test_info_with_results_single_1(test_data) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    resp = client.get(f"/dramas/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id

    fields = [
        "title",
        "link",
        "production_year_link",
        "production_year",
        "release_date",
        "playback_time",
        "country_of_origin",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") == pytest.approx(get_json_val(test_data, "$.mark_count"), abs=500)
    assert get_json_val(resp_data, "$.data.clip_count") == pytest.approx(get_json_val(test_data, "$.clip_count"), abs=500)

    assert get_json_val(resp_data, "$.data.original_title") is None
    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.genre") is None
    assert get_json_val(resp_data, "$.data.creator") is None
    assert get_json_val(resp_data, "$.data.planner") is None
    assert get_json_val(resp_data, "$.data.producer") is None
    assert get_json_val(resp_data, "$.data.executive_producer") is None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "魔女ユヒ",
            "original_title": "마녀유희",
            "rating": 3.5,
            "mark_count": 49,
            "clip_count": 13,
            "series_id": 11358,
            "season_id": 15763,
            "link": "https://filmarks.com/dramas/11358/15763",
            "production_year_link": "https://filmarks.com/list-drama/year/2000s/2007",
            "production_year": 2007,
            "country_of_origin": [
                {
                    "name": "韓国",
                    "id": 147,
                    "link": "https://filmarks.com/list-drama/country/147",
                }
            ],
            "cast": [
                {
                    "name": "ハン・ガイン",
                    "character": "マ･ユヒ",
                    "id": 175097,
                    "link": "https://filmarks.com/people/175097",
                },
                {
                    "name": "ジェヒ",
                    "character": "チェ･ムリョン",
                    "id": 4988,
                    "link": "https://filmarks.com/people/4988",
                },
                {
                    "name": "キム・ジョンフン",
                    "character": "ユ･ジュナ",
                    "id": 91733,
                    "link": "https://filmarks.com/people/91733",
                },
                {
                    "name": "チョン・ヘビン",
                    "character": "ナム･スンミ",
                    "id": 74428,
                    "link": "https://filmarks.com/people/74428",
                },
                {
                    "name": "ピョン・ヒボン",
                    "character": "マ会長",
                    "id": 50683,
                    "link": "https://filmarks.com/people/50683",
                },
                {
                    "name": "アン・ソクファン",
                    "character": "チェ･ビョンソ",
                    "id": 185994,
                    "link": "https://filmarks.com/people/185994",
                },
                {
                    "name": "イ・チェヨン",
                    "id": 194890,
                    "link": "https://filmarks.com/people/194890",
                },
                {
                    "name": "ソン・ドンイル",
                    "character": "イ･チーフ",
                    "id": 176298,
                    "link": "https://filmarks.com/people/176298",
                },
                {
                    "name": "パク・ボヨン",
                    "id": 85588,
                    "link": "https://filmarks.com/people/85588",
                },
            ],
        },
    ],
)
def test_info_with_results_single_2(test_data) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    resp = client.get(f"/dramas/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id

    fields = [
        "title",
        "original_title",
        "link",
        "production_year_link",
        "production_year",
        "country_of_origin",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") == pytest.approx(get_json_val(test_data, "$.mark_count"), abs=500)
    assert get_json_val(resp_data, "$.data.clip_count") == pytest.approx(get_json_val(test_data, "$.clip_count"), abs=500)

    assert get_json_val(resp_data, "$.data.synopsis") is None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.release_date") is None
    assert get_json_val(resp_data, "$.data.playback_time") is None
    assert get_json_val(resp_data, "$.data.genre") is None
    assert get_json_val(resp_data, "$.data.creator") is None
    assert get_json_val(resp_data, "$.data.planner") is None
    assert get_json_val(resp_data, "$.data.producer") is None
    assert get_json_val(resp_data, "$.data.executive_producer") is None
    assert get_json_val(resp_data, "$.data.director") is None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "プリズン・ブレイク",
            "original_title": "Prison Break Season 1",
            "rating": 4.4,
            "mark_count": 32153,
            "clip_count": 10559,
            "series_id": 88,
            "season_id": 335,
            "link": "https://filmarks.com/dramas/88/335",
            "poster": "https://d2ueuvlup6lbue.cloudfront.net/variants/production/store/fitpad/520/728/w7jq3266nw2prtezaccj8i6nnlgd/_.jpg",
            "production_year_link": "https://filmarks.com/list-drama/year/2000s/2005",
            "production_year": 2005,
            "playback_time": "43分",
            "country_of_origin": [
                {
                    "name": "アメリカ",
                    "id": 5,
                    "link": "https://filmarks.com/list-drama/country/5",
                }
            ],
            "cast": [
                {
                    "name": "ウェントワース・ミラー",
                    "character": "マイケル・スコフィールド",
                    "id": 19531,
                    "link": "https://filmarks.com/people/19531",
                },
                {
                    "name": "ドミニク・パーセル",
                    "character": "リンカーン・バローズ",
                    "id": 2622,
                    "link": "https://filmarks.com/people/2622",
                },
                {
                    "name": "ピーター・ストーメア",
                    "character": "ジョン・アブルッチ",
                    "id": 182555,
                    "link": "https://filmarks.com/people/182555",
                },
                {
                    "name": "ロバート・ネッパー",
                    "character": "セオドア・“ティーバッグ”・バッグウェル",
                    "id": 52665,
                    "link": "https://filmarks.com/people/52665",
                },
                {
                    "name": "アマウリー・ノラスコ",
                    "character": "フェルナンド・スクレ",
                    "id": 18339,
                    "link": "https://filmarks.com/people/18339",
                },
                {
                    "name": "ミューズ・ワトソン",
                    "character": "チャールズ・ウエストモアランド",
                    "id": 137504,
                    "link": "https://filmarks.com/people/137504",
                },
                {
                    "name": "ステイシー・キーチ",
                    "character": "ヘンリー・ポープ刑務所長",
                    "id": 177702,
                    "link": "https://filmarks.com/people/177702",
                },
                {
                    "name": "サラ・ウェイン・キャリーズ",
                    "character": "サラ・タンクレディ医師",
                    "id": 84424,
                    "link": "https://filmarks.com/people/84424",
                },
                {
                    "name": "ウェイド・ウィリアムズ",
                    "character": "ブラッド・ベリック刑務長",
                    "id": 7781,
                    "link": "https://filmarks.com/people/7781",
                },
                {
                    "name": "ロビン・タニー",
                    "character": "ベロニカ・ドノバン",
                    "id": 116127,
                    "link": "https://filmarks.com/people/116127",
                },
                {
                    "name": "マーシャル・オールマン",
                    "character": "LJ・バローズ",
                    "id": 64759,
                    "link": "https://filmarks.com/people/64759",
                },
                {
                    "name": "フランク・グリロ",
                    "character": "ニック・サブリン",
                    "id": 77096,
                    "link": "https://filmarks.com/people/77096",
                },
                {
                    "name": "ポール・アデルスタイン",
                    "character": "シークレットサービス　ケラーマン捜査官",
                    "id": 127871,
                    "link": "https://filmarks.com/people/127871",
                },
            ],
        },
    ],
)
def test_info_with_results_single_3(test_data) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    resp = client.get(f"/dramas/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id

    fields = [
        "title",
        "original_title",
        "link",
        "production_year_link",
        "production_year",
        "playback_time",
        "country_of_origin",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") == pytest.approx(get_json_val(test_data, "$.mark_count"), abs=500)
    assert get_json_val(resp_data, "$.data.clip_count") == pytest.approx(get_json_val(test_data, "$.clip_count"), abs=500)

    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.release_date") is None
    assert get_json_val(resp_data, "$.data.genre") is not None
    assert get_json_val(resp_data, "$.data.creator") is None
    assert get_json_val(resp_data, "$.data.planner") is None
    assert get_json_val(resp_data, "$.data.producer") is not None
    assert get_json_val(resp_data, "$.data.executive_producer") is not None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is None


def test_info_with_results_random() -> None:
    with open(file="tests/drama/100_dramas.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        drama = choice(test_data)

    series_id = get_json_val(drama, "$.series")
    season_id = get_json_val(drama, "$.season")

    resp = client.get(f"/dramas/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.title") is not None
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.mark_count") is not None
    assert get_json_val(resp_data, "$.data.clip_count") is not None
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert get_json_val(resp_data, "$.data.link") is not None
