from random import choice
from tests.conftest import get_json_val, get_reviews_last_page, ANIME_ENG
import json
import pytest


@pytest.mark.parametrize("path", [
    "abc/xyz",
    "2592/t",
    "hi/3304",
    "２５９２/3304",
    "2592/３３０４",
])
def test_info_input_not_valid_integer(client_nc, path) -> None:
    resp = client_nc.get(f"/animes/{path}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize("path", [
    ("abc/xyz", ""),
    ("2592/t", ""),
    ("hi/3304", ""),
    ("２５９２/3304", ""),
    ("2592/３３０４", ""),
    ("2592/3304", "?page"),
    ("2592/3304", "?page="),
    ("2592/3304", "?page=def"),
    ("2592/3304", "?page=２"),
])
def test_review_input_not_valid_integer(client_nc, path) -> None:
    resp = client_nc.get(f"/animes/{path[0]}/reviews{path[1]}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize("path", [
    ("2592/3304", "?page=0"),
])
def test_review_input_less_than_min_threshold(client_nc, path) -> None:
    resp = client_nc.get(f"/animes/{path[0]}/reviews{path[1]}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be greater than 0"


@pytest.mark.parametrize("path", [
    ("2592/3304", "?page=10001"),
])
def test_review_input_more_than_max_threshold(client_nc, path) -> None:
    resp = client_nc.get(f"/animes/{path[0]}/reviews{path[1]}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be less than or equal to 10000"


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "デジモンアドベンチャー",
            "rating": 4.3,
            "mark_count": 2293,
            "clip_count": 587,
            "series_id": 2592,
            "season_id": 3304,
            "link": "https://filmarks.com/animes/2592/3304",
            "production_year_link": "https://filmarks.com/list-anime/year/1990s/1999",
            "production_year": 1999,
            "release_date": "1999年03月07日",
            "playback_time": "23分",
            "country_of_origin": ["日本"],
            "production_company": [
                {
                    "name": "東映アニメーション",
                    "id": 41,
                    "link": "https://filmarks.com/list-anime/company/41",
                }
            ],
            "cast": [
                {
                    "name": "藤田淑子",
                    "character": "八神太一",
                    "id": 44556,
                    "link": "https://filmarks.com/people/44556",
                },
                {
                    "name": "坂本千夏",
                    "character": "アグモン",
                    "id": 122276,
                    "link": "https://filmarks.com/people/122276",
                },
                {
                    "name": " 風間勇刀",
                    "character": "石田ヤマト",
                    "id": 240716,
                    "link": "https://filmarks.com/people/240716",
                },
                {
                    "name": "山口眞弓",
                    "character": "ガブモン",
                    "id": 214280,
                    "link": "https://filmarks.com/people/214280",
                },
                {
                    "name": "水谷優子",
                    "character": "武之内空",
                    "id": 214749,
                    "link": "https://filmarks.com/people/214749",
                },
                {
                    "name": "重松花鳥",
                    "character": "ピヨモン",
                    "id": 214279,
                    "link": "https://filmarks.com/people/214279",
                },
                {
                    "name": "天神有海",
                    "character": "泉光子郎",
                    "id": 240715,
                    "link": "https://filmarks.com/people/240715",
                },
                {
                    "name": "櫻井孝宏",
                    "character": "テントモン",
                    "id": 187531,
                    "link": "https://filmarks.com/people/187531",
                },
                {
                    "name": "前田愛",
                    "character": "太刀川ミミ",
                    "id": 274563,
                    "link": "https://filmarks.com/people/274563",
                },
                {
                    "name": "山田きのこ",
                    "character": "パルモン",
                    "id": 214281,
                    "link": "https://filmarks.com/people/214281",
                },
                {
                    "name": "菊池正美",
                    "character": "城戸丈",
                    "id": 220563,
                    "link": "https://filmarks.com/people/220563",
                },
                {
                    "name": "竹内順子",
                    "character": "ゴマモン",
                    "id": 189557,
                    "link": "https://filmarks.com/people/189557",
                },
                {
                    "name": "小西寛子",
                    "character": "高石タケル",
                    "id": 240717,
                    "link": "https://filmarks.com/people/240717",
                },
                {
                    "name": "松本美和",
                    "character": "パタモン",
                    "id": 75432,
                    "link": "https://filmarks.com/people/75432",
                },
                {
                    "name": "荒木香恵",
                    "character": "八神ヒカリ",
                    "id": 237819,
                    "link": "https://filmarks.com/people/237819",
                },
                {
                    "name": "徳光由禾",
                    "character": "テイルモン",
                    "id": 214282,
                    "link": "https://filmarks.com/people/214282",
                },
            ],
        },
    ],
)
def test_info_with_results_single_1(client_nc, test_data, caplog) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    resp = client_nc.get(f"/animes/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert ANIME_ENG in caplog.text

    fields = [
        "title",
        "link",
        "production_year_link",
        "production_year",
        "release_date",
        "playback_time",
        "country_of_origin",
        "production_company",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(resp_data, "$.data.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(resp_data, "$.data.original_title") is None
    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.official_site") is None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.creator") is not None
    assert get_json_val(resp_data, "$.data.planner") is None
    assert get_json_val(resp_data, "$.data.producer") is None
    assert get_json_val(resp_data, "$.data.executive_producer") is None
    assert get_json_val(resp_data, "$.data.chief_director") is None
    assert get_json_val(resp_data, "$.data.director") is None
    assert get_json_val(resp_data, "$.data.series_composer") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.character_original_designer") is None
    assert get_json_val(resp_data, "$.data.character_designer") is not None
    assert get_json_val(resp_data, "$.data.narrator") is not None
    assert get_json_val(resp_data, "$.data.artist") is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "DEATH NOTE",
            "rating": 4.3,
            "mark_count": 14633,
            "clip_count": 3233,
            "series_id": 1533,
            "season_id": 2046,
            "link": "https://filmarks.com/animes/1533/2046",
            "production_year_link": "https://filmarks.com/list-anime/year/2000s/2006",
            "production_year": 2006,
            "release_date": "2006年10月04日",
            "country_of_origin": ["日本"],
            "production_company": [
                {
                    "name": "マッドハウス",
                    "id": 43,
                    "link": "https://filmarks.com/list-anime/company/43",
                }
            ],
            "cast": [
                {
                    "name": "宮野真守",
                    "character": "夜神月",
                    "id": 52736,
                    "link": "https://filmarks.com/people/52736",
                },
                {
                    "name": "山口勝平",
                    "character": "L",
                    "id": 123348,
                    "link": "https://filmarks.com/people/123348",
                },
                {
                    "name": "日髙のり子",
                    "character": "ニア",
                    "id": 271949,
                    "link": "https://filmarks.com/people/271949",
                },
                {
                    "name": "佐々木望",
                    "character": "メロ",
                    "id": 158771,
                    "link": "https://filmarks.com/people/158771",
                },
                {
                    "name": "平野綾",
                    "character": "弥海砂 ",
                    "id": 186905,
                    "link": "https://filmarks.com/people/186905",
                },
                {
                    "name": "松風雅也",
                    "character": "魅上照",
                    "id": 143856,
                    "link": "https://filmarks.com/people/143856",
                },
                {
                    "name": "岡村麻純",
                    "character": "高田清美",
                    "id": 275804,
                    "link": "https://filmarks.com/people/275804",
                },
            ],
        },
    ],
)
def test_info_with_results_single_2(client_nc, test_data, caplog) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    resp = client_nc.get(f"/animes/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert ANIME_ENG in caplog.text

    fields = [
        "title",
        "link",
        "production_year_link",
        "production_year",
        "release_date",
        "playback_time",
        "country_of_origin",
        "production_company",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(resp_data, "$.data.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(resp_data, "$.data.original_title") is None
    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.official_site") is None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.creator") is not None
    assert get_json_val(resp_data, "$.data.planner") is None
    assert get_json_val(resp_data, "$.data.producer") is None
    assert get_json_val(resp_data, "$.data.executive_producer") is None
    assert get_json_val(resp_data, "$.data.chief_director") is None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.series_composer") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is None
    assert get_json_val(resp_data, "$.data.character_original_designer") is None
    assert get_json_val(resp_data, "$.data.character_designer") is not None
    assert get_json_val(resp_data, "$.data.narrator") is None
    assert get_json_val(resp_data, "$.data.artist") is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "アバター 伝説の少年アン：火の巻",
            "original_title": "Avatar: The Last Airbender：Fire",
            "rating": 4.5,
            "mark_count": 75,
            "clip_count": 37,
            "series_id": 3691,
            "season_id": 4983,
            "link": "https://filmarks.com/animes/3691/4983",
            "production_year_link": "https://filmarks.com/list-anime/year/2000s/2007",
            "production_year": 2007,
            "country_of_origin": ["アメリカ"],
            "production_company": [
                {
                    "name": "MOI Animation",
                    "id": 432,
                    "link": "https://filmarks.com/list-anime/company/432",
                }
            ],
            "cast": [
                {
                    "name": "ザック・タイラー",
                    "character": "アン",
                    "id": 47745,
                    "link": "https://filmarks.com/people/47745",
                },
                {
                    "name": "メイ・ホイットマン",
                    "character": "カタラ",
                    "id": 12018,
                    "link": "https://filmarks.com/people/12018",
                },
                {
                    "name": "ジャック・デ・セナ",
                    "character": "サカ",
                    "id": 231429,
                    "link": "https://filmarks.com/people/231429",
                },
                {
                    "name": "ディー・ブラッドリー・ベイカー",
                    "character": "アッパ／モモ",
                    "id": 192081,
                    "link": "https://filmarks.com/people/192081",
                },
                {
                    "name": "ダンテ・バスコ",
                    "character": "ズーコ",
                    "id": 123497,
                    "link": "https://filmarks.com/people/123497",
                },
                {
                    "name": "ジェシー・フラワー",
                    "character": "トフ",
                    "id": 307449,
                    "link": "https://filmarks.com/people/307449",
                },
            ],
        },
    ],
)
def test_info_with_results_single_3(client_nc, test_data, caplog) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    resp = client_nc.get(f"/animes/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert ANIME_ENG in caplog.text

    fields = [
        "title",
        "original_title",
        "link",
        "production_year_link",
        "production_year",
        "country_of_origin",
        "production_company",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(resp_data, "$.data.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.official_site") is None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.release_date") is None
    assert get_json_val(resp_data, "$.data.playback_time") is None
    assert get_json_val(resp_data, "$.data.creator") is None
    assert get_json_val(resp_data, "$.data.planner") is None
    assert get_json_val(resp_data, "$.data.producer") is None
    assert get_json_val(resp_data, "$.data.executive_producer") is not None
    assert get_json_val(resp_data, "$.data.chief_director") is None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.series_composer") is None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.character_original_designer") is None
    assert get_json_val(resp_data, "$.data.character_designer") is None
    assert get_json_val(resp_data, "$.data.narrator") is None
    assert get_json_val(resp_data, "$.data.artist") is None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "ドラゴンボールDAIMA",
            "rating": 3.7,
            "mark_count": 2119,
            "clip_count": 1681,
            "series_id": 4304,
            "season_id": 5798,
            "link": "https://filmarks.com/animes/4304/5798",
            "official_site": "https://dragonballdaima.com/",
            "production_year_link": "https://filmarks.com/list-anime/year/2020s/2024",
            "production_year": 2024,
            "release_date": "2024年10月11日",
            "playback_time": "24分",
            "country_of_origin": ["日本"],
            "production_company": [
                {
                    "name": "東映アニメーション",
                    "id": 41,
                    "link": "https://filmarks.com/list-anime/company/41",
                }
            ],
            "cast": [
                {
                    "name": "野沢雅子",
                    "character": "孫悟空（ミニ）",
                    "id": 186719,
                    "link": "https://filmarks.com/people/186719",
                },
                {
                    "name": "小林由美子",
                    "character": "界王神（ミニ）",
                    "id": 208464,
                    "link": "https://filmarks.com/people/208464",
                },
                {
                    "name": "内山昂輝",
                    "character": "グロリオ",
                    "id": 195165,
                    "link": "https://filmarks.com/people/195165",
                },
                {
                    "name": "ファイルーズあい",
                    "character": "パンジ",
                    "id": 263130,
                    "link": "https://filmarks.com/people/263130",
                },
                {
                    "name": "森久保祥太郎",
                    "character": "ゴマー",
                    "id": 11386,
                    "link": "https://filmarks.com/people/11386",
                },
                {
                    "name": "榎木淳弥",
                    "character": "デゲス",
                    "id": 207207,
                    "link": "https://filmarks.com/people/207207",
                },
                {
                    "name": "日笠陽子",
                    "character": "ドクター・アリンス",
                    "id": 60508,
                    "link": "https://filmarks.com/people/60508",
                },
                {
                    "name": "中原麻衣",
                    "character": "ブルマ（ミニ）",
                    "id": 203624,
                    "link": "https://filmarks.com/people/203624",
                },
                {
                    "name": "三野雄大",
                    "character": "ベジータ（ミニ）",
                    "id": 338759,
                    "link": "https://filmarks.com/people/338759",
                },
                {
                    "name": "山口智広",
                    "character": "ピッコロ（ミニ）",
                    "id": 285590,
                    "link": "https://filmarks.com/people/285590",
                },
                {
                    "name": "金田アキ",
                    "character": "クリリン（ミニ）",
                    "id": 261431,
                    "link": "https://filmarks.com/people/261431",
                },
                {
                    "name": "加隈亜衣",
                    "character": "チチ（ミニ）",
                    "id": 204901,
                    "link": "https://filmarks.com/people/204901",
                },
                {
                    "name": "金光宣明",
                    "character": "亀仙人（ミニ）",
                    "id": 221653,
                    "link": "https://filmarks.com/people/221653",
                },
                {
                    "name": "代永翼",
                    "character": "トランクス（ミニ）",
                    "id": 194769,
                    "link": "https://filmarks.com/people/194769",
                },
                {
                    "name": "後藤恵里菜",
                    "character": "デンデ（ミニ）",
                    "id": 303130,
                    "link": "https://filmarks.com/people/303130",
                },
                {
                    "name": "斉藤貴美子",
                    "character": "ミスター・ポポ（ミニ）",
                    "id": 223025,
                    "link": "https://filmarks.com/people/223025",
                },
                {
                    "name": "半田裕典",
                    "character": "キビト（ミニ）",
                    "id": 350013,
                    "link": "https://filmarks.com/people/350013",
                },
                {
                    "name": "櫻井トオル",
                    "character": "ミスター・サタン（ミニ）",
                    "id": 274168,
                    "link": "https://filmarks.com/people/274168",
                },
                {
                    "name": "安室志穂",
                    "character": "魔人ブウ（ミニ）",
                    "id": 350014,
                    "link": "https://filmarks.com/people/350014",
                },
                {
                    "name": "関智一",
                    "character": "魔人クウ",
                    "id": 9579,
                    "link": "https://filmarks.com/people/9579",
                },
                {
                    "name": "三宅健太",
                    "character": "タマガミ・ナンバー・スリー",
                    "id": 115581,
                    "link": "https://filmarks.com/people/115581",
                },
                {
                    "name": "堀越真己",
                    "character": "大魔女マーバ",
                    "id": 187707,
                    "link": "https://filmarks.com/people/187707",
                },
                {
                    "name": "れいみ",
                    "character": "ハイビス",
                    "id": 303252,
                    "link": "https://filmarks.com/people/303252",
                },
                {
                    "name": "中博史",
                    "character": "ネバ",
                    "id": 216286,
                    "link": "https://filmarks.com/people/216286",
                },
                {
                    "name": "落合福嗣",
                    "character": "魔人ドゥー",
                    "id": 211346,
                    "link": "https://filmarks.com/people/211346",
                },
            ],
        },
    ],
)
def test_info_with_results_single_4(client_nc, test_data, caplog) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    resp = client_nc.get(f"/animes/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert ANIME_ENG in caplog.text

    fields = [
        "title",
        "link",
        "official_site",
        "production_year_link",
        "production_year",
        "release_date",
        "playback_time",
        "country_of_origin",
        "production_company",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(resp_data, "$.data.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(resp_data, "$.data.original_title") is None
    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.creator") is not None
    assert get_json_val(resp_data, "$.data.planner") is None
    assert get_json_val(resp_data, "$.data.producer") is None
    assert get_json_val(resp_data, "$.data.executive_producer") is None
    assert get_json_val(resp_data, "$.data.chief_director") is None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.series_composer") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.character_original_designer") is None
    assert get_json_val(resp_data, "$.data.character_designer") is not None
    assert get_json_val(resp_data, "$.data.narrator") is None
    assert get_json_val(resp_data, "$.data.artist") is not None


def test_info_with_results_random(client_nc, caplog) -> None:
    with open(file="tests/anime/100_animes.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        anime = choice(test_data)

    title = get_json_val(anime, "$.title")
    series_id = get_json_val(anime, "$.series")
    season_id = get_json_val(anime, "$.season")

    resp = client_nc.get(f"/animes/{series_id}/{season_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert ANIME_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.mark_count") is not None
    assert get_json_val(resp_data, "$.data.clip_count") is not None
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert get_json_val(resp_data, "$.data.link") is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "DEATH NOTE",
            "rating": 4.3,
            "series_id": 1533,
            "season_id": 2046,
            "link": "https://filmarks.com/animes/1533/2046",
            "reviews": {
                "user": {
                    "name": "ChameleonBaby",
                    "id": "Nick575",
                    "link": "https://filmarks.com/users/Nick575",
                },
                "review": {
                    "date": "2020/11/20 19:29",
                    "rating": 4,
                    "id": 292787,
                    "link": "https://filmarks.com/animes/1533/2046/reviews/292787",
                    "contents": "原作が素晴らしいが、アニメ化も素晴らしかった。 特にシブタクの人気が圧倒的。 数々のMAD素材にもなったことから、当時のニコニコ動画文化に根強く浸透している。",
                },
            },
        },
    ],
)
def test_review_with_results_full(client_nc, test_data, caplog) -> None:
    series_id = get_json_val(test_data, "$.series_id")
    season_id = get_json_val(test_data, "$.season_id")

    slug = f"animes/{series_id}/{season_id}"
    last_page = get_reviews_last_page(slug)

    resp = client_nc.get(f"{slug}/reviews?page={last_page}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert ANIME_ENG in caplog.text

    review_fields = [
        "user.name",
        "user.id",
        "user.link",
        "review.date",
        "review.rating",
        "review.id",
        "review.link",
        "review.contents"
    ]
    for field in review_fields:
        assert get_json_val(resp_data, f"$.data.reviews[-1].{field}") == get_json_val(test_data, f"$.reviews.{field}")

    assert get_json_val(resp_data, "$.data.title") == get_json_val(test_data, "$.title")
    assert get_json_val(resp_data, "$.data.original_title") is None
    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.link") == f"{get_json_val(test_data, "$.link")}?page={last_page}"
    assert len(get_json_val(resp_data, "$.data.reviews")) > 0


def test_review_with_results(client_nc, caplog) -> None:
    title = "ラグラッツ シーズン1"
    original_title = "Rugrats Season 1"
    series_id = 3980
    season_id = 5380

    resp = client_nc.get(f"/animes/{series_id}/{season_id}/reviews")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert ANIME_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.original_title") == original_title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert get_json_val(resp_data, "$.data.link") is not None
    assert len(get_json_val(resp_data, "$.data.reviews")) > 0


def test_review_without_results(client_nc, caplog) -> None:
    title = "ラグラッツ シーズン1"
    original_title = "Rugrats Season 1"
    series_id = 3980
    season_id = 5380

    resp = client_nc.get(f"/animes/{series_id}/{season_id}/reviews?page=10")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert ANIME_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.original_title") == original_title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert get_json_val(resp_data, "$.data.link") is not None
    assert len(get_json_val(resp_data, "$.data.reviews")) == 0


def test_review_with_results_random(client_nc, caplog) -> None:
    with open(file="tests/anime/100_animes.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        anime = choice(test_data)

    title = get_json_val(anime, "$.title")
    series_id = get_json_val(anime, "$.series")
    season_id = get_json_val(anime, "$.season")

    resp = client_nc.get(f"/animes/{series_id}/{season_id}/reviews")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert ANIME_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.series_id") == series_id
    assert get_json_val(resp_data, "$.data.season_id") == season_id
    assert get_json_val(resp_data, "$.data.link") is not None
    assert len(get_json_val(resp_data, "$.data.reviews")) > 0
