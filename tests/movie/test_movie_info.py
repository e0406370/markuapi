from random import choice
from tests.conftest import get_json_val, get_reviews_last_page, MOVIE_ENG
import json
import pytest


@pytest.mark.parametrize("path", [
    "abc"
    "１４３４８",
])
def test_info_input_not_valid_integer(client_nc, path) -> None:
    resp = client_nc.get(f"/movies/{path}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize("path", [
    ("abc", ""),
    ("１４３４８", ""),
    ("14348", "?page"),
    ("14348", "?page="),
    ("14348", "?page=def"),
    ("14348", "?page=２"),
])
def test_review_input_not_valid_integer(client_nc, path) -> None:
    resp = client_nc.get(f"/movies/{path[0]}/reviews{path[1]}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize("path", [
    ("14348", "?page=0"),
])
def test_review_input_less_than_min_threshold(client_nc, path) -> None:
    resp = client_nc.get(f"/movies/{path[0]}/reviews{path[1]}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be greater than 0"


@pytest.mark.parametrize("path", [
    ("14348", "?page=10001"),
])
def test_review_input_more_than_max_threshold(client_nc, path) -> None:
    resp = client_nc.get(f"/movies/{path[0]}/reviews{path[1]}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be less than or equal to 10000"

@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "ダークナイト",
            "original_title": "The Dark Knight",
            "rating": 4.2,
            "mark_count": 206293,
            "clip_count": 47035,
            "movie_id": 33832,
            "link": "https://filmarks.com/movies/33832",
            "production_year_link": "https://filmarks.com/list/year/2000s/2008",
            "production_year": 2008,
            "screening_date": "2008年08月09日",
            "screening_time": "152分",
            "country_of_origin": [
                {
                    "name": "アメリカ",
                    "id": 5,
                    "link": "https://filmarks.com/list/country/5",
                }
            ],
            "cast": [
                {
                    "name": "クリスチャン・ベイル",
                    "character": "ブルース・ウェイン／バットマン",
                    "id": 179790,
                    "link": "https://filmarks.com/people/179790",
                },
                {
                    "name": "ヒース・レジャー",
                    "character": "ジョーカー",
                    "id": 96468,
                    "link": "https://filmarks.com/people/96468",
                },
                {
                    "name": "アーロン・エッカート",
                    "character": "ハービー・デント",
                    "id": 95575,
                    "link": "https://filmarks.com/people/95575",
                },
                {
                    "name": "マイケル・ケイン",
                    "character": "アルフレッド・ペニーワース",
                    "id": 129698,
                    "link": "https://filmarks.com/people/129698",
                },
                {
                    "name": "マギー・ギレンホール",
                    "character": "レイチェル・ドーズ",
                    "id": 76276,
                    "link": "https://filmarks.com/people/76276",
                },
                {
                    "name": "ゲイリー・オールドマン",
                    "character": "ジェームズ・“ジム”・ゴードン",
                    "id": 76854,
                    "link": "https://filmarks.com/people/76854",
                },
                {
                    "name": "モーガン・フリーマン",
                    "character": "ルーシャス・フォックス",
                    "id": 162058,
                    "link": "https://filmarks.com/people/162058",
                },
                {
                    "name": "モニーク・ガブリエラ・カーネン",
                    "character": "アンナ・ラミレス",
                    "id": 169378,
                    "link": "https://filmarks.com/people/169378",
                },
                {
                    "name": "ロン・ディーン",
                    "character": "マイケル・ワーツ",
                    "id": 168827,
                    "link": "https://filmarks.com/people/168827",
                },
                {
                    "name": "キリアン・マーフィ",
                    "character": "ジョナサン・クレイン",
                    "id": 32549,
                    "link": "https://filmarks.com/people/32549",
                },
                {
                    "name": "チン・ハン",
                    "character": "ラウ",
                    "id": 115241,
                    "link": "https://filmarks.com/people/115241",
                },
                {
                    "name": "ネスター・カーボネル",
                    "character": "アンソニー・ガルシア",
                    "id": 9875,
                    "link": "https://filmarks.com/people/9875",
                },
                {
                    "name": "エリック・ロバーツ",
                    "character": "サルバトーレ・マローニ",
                    "id": 32191,
                    "link": "https://filmarks.com/people/32191",
                },
                {
                    "name": "リッチー・コスター",
                    "character": "チェチェン人ボス",
                    "id": 17553,
                    "link": "https://filmarks.com/people/17553",
                },
                {
                    "name": "アンソニー・マイケル・ホール",
                    "character": "マイク・エンゲル",
                    "id": 157131,
                    "link": "https://filmarks.com/people/157131",
                },
                {
                    "name": "キース・ザラバッカ",
                    "character": "ジェラルド・スティーブンズ",
                    "id": 403,
                    "link": "https://filmarks.com/people/403",
                },
                {
                    "name": "コリン・マクファーレン",
                    "character": "ギリアン・B・ローブ",
                    "id": 166180,
                    "link": "https://filmarks.com/people/166180",
                },
                {
                    "name": "ジョシュア・ハート",
                    "character": "コールマン・リース",
                    "id": 138739,
                    "link": "https://filmarks.com/people/138739",
                },
                {
                    "name": "メリンダ・マックグロウ",
                    "character": "バーバラ・ゴードン",
                    "id": 118531,
                    "link": "https://filmarks.com/people/118531",
                },
                {
                    "name": "ネイサン・ギャンブル",
                    "character": "ジェームズ・“ジミー”・ゴードン・Jr",
                    "id": 58815,
                    "link": "https://filmarks.com/people/58815",
                },
                {
                    "name": "マイケル・ジェイ・ホワイト",
                    "character": "ギャンボル",
                    "id": 35406,
                    "link": "https://filmarks.com/people/35406",
                },
                {
                    "name": "ウィリアム・フィクナー",
                    "character": "銀行支店長",
                    "id": 4099,
                    "link": "https://filmarks.com/people/4099",
                },
                {
                    "name": "マシュー・オニール",
                    "character": "チャクルズ",
                    "id": 55502,
                    "link": "https://filmarks.com/people/55502",
                },
                {
                    "name": "エディソン・チャン",
                    "id": 74619,
                    "link": "https://filmarks.com/people/74619",
                },
                {
                    "name": "マイケル・ストヤノフ",
                    "character": "ドーピー",
                    "id": 159085,
                    "link": "https://filmarks.com/people/159085",
                },
                {
                    "name": "デヴィッド・ダストマルチャン",
                    "character": "トーマス・シフ",
                    "id": 191423,
                    "link": "https://filmarks.com/people/191423",
                },
            ],
        },
    ],
)
def test_info_with_results_single_1(client_nc, test_data, caplog) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    resp = client_nc.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert MOVIE_ENG in caplog.text

    fields = [
        "title",
        "original_title",
        "link",
        "production_year_link",
        "production_year",
        "screening_date",
        "screening_time",
        "country_of_origin",
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
    assert get_json_val(resp_data, "$.data.genre") is not None
    assert get_json_val(resp_data, "$.data.distributor") is not None
    assert get_json_val(resp_data, "$.data.creator") is None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "サバイバルファミリー",
            "rating": 3.5,
            "mark_count": 55551,
            "clip_count": 13780,
            "movie_id": 69153,
            "link": "https://filmarks.com/movies/69153",
            "production_year_link": "https://filmarks.com/list/year/2010s/2017",
            "production_year": 2017,
            "screening_date": "2017年02月11日",
            "screening_time": "117分",
            "country_of_origin": [
                {
                    "name": "日本",
                    "id": 144,
                    "link": "https://filmarks.com/list/country/144",
                }
            ],
            "cast": [
                {
                    "name": "小日向文世",
                    "character": "鈴木義之",
                    "id": 51000,
                    "link": "https://filmarks.com/people/51000",
                },
                {
                    "name": "深津絵里",
                    "character": "鈴木光恵",
                    "id": 143090,
                    "link": "https://filmarks.com/people/143090",
                },
                {
                    "name": "泉澤祐希",
                    "character": "鈴木賢司",
                    "id": 186288,
                    "link": "https://filmarks.com/people/186288",
                },
                {
                    "name": "葵わかな",
                    "character": "鈴木結衣",
                    "id": 192162,
                    "link": "https://filmarks.com/people/192162",
                },
                {
                    "name": "菅原大吉",
                    "id": 163124,
                    "link": "https://filmarks.com/people/163124",
                },
                {
                    "name": "徳井優",
                    "id": 90668,
                    "link": "https://filmarks.com/people/90668",
                },
                {
                    "name": "桂雀々",
                    "id": 136172,
                    "link": "https://filmarks.com/people/136172",
                },
                {
                    "name": "森下能幸",
                    "id": 35127,
                    "link": "https://filmarks.com/people/35127",
                },
                {
                    "name": "田中要次",
                    "id": 154675,
                    "link": "https://filmarks.com/people/154675",
                },
                {
                    "name": "有福正志",
                    "id": 177514,
                    "link": "https://filmarks.com/people/177514",
                },
                {
                    "name": "左時枝",
                    "id": 55975,
                    "link": "https://filmarks.com/people/55975",
                },
                {
                    "name": "時任三郎",
                    "character": "斎藤敏夫",
                    "id": 108989,
                    "link": "https://filmarks.com/people/108989",
                },
                {
                    "name": "ミッキー・カーチス",
                    "id": 4258,
                    "link": "https://filmarks.com/people/4258",
                },
                {
                    "name": "藤原紀香",
                    "character": "斎藤静子",
                    "id": 122018,
                    "link": "https://filmarks.com/people/122018",
                },
                {
                    "name": "大野拓朗",
                    "character": "斎藤涼介",
                    "id": 64907,
                    "link": "https://filmarks.com/people/64907",
                },
                {
                    "name": "志尊淳",
                    "character": "斎藤翔平",
                    "id": 194173,
                    "link": "https://filmarks.com/people/194173",
                },
                {
                    "name": "渡辺えり",
                    "character": "古田富子",
                    "id": 91748,
                    "link": "https://filmarks.com/people/91748",
                },
                {
                    "name": "宅麻伸",
                    "character": "高橋亮三",
                    "id": 126115,
                    "link": "https://filmarks.com/people/126115",
                },
                {
                    "name": "柄本明",
                    "character": "佐々木重臣",
                    "id": 148053,
                    "link": "https://filmarks.com/people/148053",
                },
                {
                    "name": "大地康雄",
                    "character": "田中善一",
                    "id": 65017,
                    "link": "https://filmarks.com/people/65017",
                },
            ],
        },
    ],
)
def test_info_with_results_single_2(client_nc, test_data, caplog) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    resp = client_nc.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert MOVIE_ENG in caplog.text

    fields = [
        "title",
        "link",
        "production_year_link",
        "production_year",
        "screening_date",
        "screening_time",
        "country_of_origin",
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
    assert get_json_val(resp_data, "$.data.genre") is not None
    assert get_json_val(resp_data, "$.data.distributor") is not None
    assert get_json_val(resp_data, "$.data.creator") is not None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "ハリー・ポッターと死の秘宝 PART1",
            "original_title": "Harry Potter and the Deathly Hallows: Part 1",
            "rating": 3.9,
            "mark_count": 211876,
            "clip_count": 12594,
            "movie_id": 27701,
            "link": "https://filmarks.com/movies/27701",
            "production_year_link": "https://filmarks.com/list/year/2010s/2010",
            "production_year": 2010,
            "screening_date": "2010年11月19日",
            "screening_time": "146分",
            "country_of_origin": [
                {
                    "name": "イギリス",
                    "id": 11,
                    "link": "https://filmarks.com/list/country/11",
                },
                {
                    "name": "アメリカ",
                    "id": 5,
                    "link": "https://filmarks.com/list/country/5",
                },
            ],
            "cast": [
                {
                    "name": "ダニエル・ラドクリフ",
                    "character": "ハリー・ポッター",
                    "id": 93709,
                    "link": "https://filmarks.com/people/93709",
                },
                {
                    "name": "ルパート・グリント",
                    "character": "ロン・ウィーズリー",
                    "id": 49543,
                    "link": "https://filmarks.com/people/49543",
                },
                {
                    "name": "エマ・ワトソン",
                    "character": "ハーマイオニー・グレンジャー",
                    "id": 181498,
                    "link": "https://filmarks.com/people/181498",
                },
                {
                    "name": "ヘレナ・ボナム=カーター",
                    "character": "ベラトリックス・レストレンジ",
                    "id": 172381,
                    "link": "https://filmarks.com/people/172381",
                },
                {
                    "name": "ロビー・コルトレーン",
                    "character": "ルビウス・ハグリッド",
                    "id": 133558,
                    "link": "https://filmarks.com/people/133558",
                },
                {
                    "name": "トム・フェルトン",
                    "character": "ドラコ・マルフォイ",
                    "id": 39284,
                    "link": "https://filmarks.com/people/39284",
                },
                {
                    "name": "レイフ・ファインズ",
                    "character": "ヴォルデモート",
                    "id": 53636,
                    "link": "https://filmarks.com/people/53636",
                },
                {
                    "name": "ブレンダン・グリーソン",
                    "character": "アラスター・ムーディ",
                    "id": 74009,
                    "link": "https://filmarks.com/people/74009",
                },
                {
                    "name": "リチャード・グリフィス",
                    "character": "バーノン・ダーズリー",
                    "id": 172595,
                    "link": "https://filmarks.com/people/172595",
                },
                {
                    "name": "ジョン・ハート",
                    "character": "オリバンダー老人",
                    "id": 141919,
                    "link": "https://filmarks.com/people/141919",
                },
                {
                    "name": "ジェイソン・アイザックス",
                    "character": "ルシウス・マルフォイ",
                    "id": 154590,
                    "link": "https://filmarks.com/people/154590",
                },
                {
                    "name": "ヘレン・マックロリー",
                    "character": "ナルシッサ・マルフォイ",
                    "id": 15531,
                    "link": "https://filmarks.com/people/15531",
                },
                {
                    "name": "ビル・ナイ",
                    "character": "ルーファス・スクリムジョール",
                    "id": 103981,
                    "link": "https://filmarks.com/people/103981",
                },
                {
                    "name": "ミランダ・リチャードソン",
                    "character": "リータ・スキーター",
                    "id": 69880,
                    "link": "https://filmarks.com/people/69880",
                },
                {
                    "name": "アラン・リックマン",
                    "character": "セブルス・スネイプ",
                    "id": 63940,
                    "link": "https://filmarks.com/people/63940",
                },
                {
                    "name": "ティモシー・スポール",
                    "character": "ピーター・ペティグリュー",
                    "id": 163849,
                    "link": "https://filmarks.com/people/163849",
                },
                {
                    "name": "イメルダ・スタウントン",
                    "character": "ドローレス・アンブリッジ",
                    "id": 131871,
                    "link": "https://filmarks.com/people/131871",
                },
                {
                    "name": "デヴィッド・シューリス",
                    "character": "リーマス・ルーピン",
                    "id": 120698,
                    "link": "https://filmarks.com/people/120698",
                },
                {
                    "name": "ジュリー・ウォルターズ",
                    "character": "モリー・ウィーズリー",
                    "id": 21241,
                    "link": "https://filmarks.com/people/21241",
                },
                {
                    "name": "ボニー・ライト",
                    "character": "ジニー・ウィーズリー",
                    "id": 56343,
                    "link": "https://filmarks.com/people/56343",
                },
                {
                    "name": "ジェームズ・フェルプス",
                    "character": "フレッド・ウィーズリー",
                    "id": 105900,
                    "link": "https://filmarks.com/people/105900",
                },
                {
                    "name": "オリヴァー・フェルプス",
                    "character": "ジョージ・ウィーズリー",
                    "id": 8433,
                    "link": "https://filmarks.com/people/8433",
                },
                {
                    "name": "サイモン・マクバーニー",
                    "character": "クリーチャー",
                    "id": 153912,
                    "link": "https://filmarks.com/people/153912",
                },
                {
                    "name": "ジョージ・ハリス",
                    "character": "キングズリー・シャックルボルト",
                    "id": 93989,
                    "link": "https://filmarks.com/people/93989",
                },
                {
                    "name": "イヴァナ・リンチ",
                    "character": "ルーナ・ラブグッド",
                    "id": 88775,
                    "link": "https://filmarks.com/people/88775",
                },
                {
                    "name": "マシュー・ルイス",
                    "character": "ネビル・ロングボトム",
                    "id": 151038,
                    "link": "https://filmarks.com/people/151038",
                },
                {
                    "name": "マーク・ウィリアムズ",
                    "character": "アーサー・ウィーズリー",
                    "id": 133352,
                    "link": "https://filmarks.com/people/133352",
                },
                {
                    "name": "ハリー・メリング",
                    "character": "ダドリー・ダーズリー",
                    "id": 154081,
                    "link": "https://filmarks.com/people/154081",
                },
                {
                    "name": "ナタリア・テナ",
                    "character": "ニンファドーラ・トンクス",
                    "id": 181255,
                    "link": "https://filmarks.com/people/181255",
                },
                {
                    "name": "クレマンス・ポエジー",
                    "character": "フラー・デラクール",
                    "id": 34868,
                    "link": "https://filmarks.com/people/34868",
                },
                {
                    "name": "デイヴ・レジーノ",
                    "id": 63516,
                    "link": "https://filmarks.com/people/63516",
                },
                {
                    "name": "ワーウィック・デイヴィス",
                    "id": 150297,
                    "link": "https://filmarks.com/people/150297",
                },
                {
                    "name": "フレディ・ストローマ",
                    "character": "コーマック・マクラーゲン",
                    "id": 49051,
                    "link": "https://filmarks.com/people/49051",
                },
                {
                    "name": "ピーター・マラン",
                    "character": "ヤックスリー",
                    "id": 1714,
                    "link": "https://filmarks.com/people/1714",
                },
                {
                    "name": "ガイ・ヘンリー",
                    "character": "パイアス・シックネス",
                    "id": 174548,
                    "link": "https://filmarks.com/people/174548",
                },
                {
                    "name": "ドーナル・グリーソン",
                    "character": "ビル・ウィーズリー",
                    "id": 144047,
                    "link": "https://filmarks.com/people/144047",
                },
                {
                    "name": "アンディ・リンデン",
                    "character": "マンダンガス・フレッチャー",
                    "id": 114138,
                    "link": "https://filmarks.com/people/114138",
                },
                {
                    "name": "リス・エヴァンス",
                    "character": "ゼノフィリウス・ラブグッド",
                    "id": 180121,
                    "link": "https://filmarks.com/people/180121",
                },
                {
                    "name": "デヴィッド・ライオール",
                    "character": "エルファイアス・ドージ",
                    "id": 96703,
                    "link": "https://filmarks.com/people/96703",
                },
                {
                    "name": "マッティエロック・ギブス",
                    "character": "ミュリエル・プルウェット",
                    "id": 108040,
                    "link": "https://filmarks.com/people/108040",
                },
                {
                    "name": "ニック・モラン",
                    "character": "スカビオール",
                    "id": 70470,
                    "link": "https://filmarks.com/people/70470",
                },
                {
                    "name": "ジェイミー・キャンベル・バウアー",
                    "character": "ゲラート・グリンデルバルド",
                    "id": 81369,
                    "link": "https://filmarks.com/people/81369",
                },
                {
                    "name": "キャロライン・ピクルズ",
                    "id": 91214,
                    "link": "https://filmarks.com/people/91214",
                },
                {
                    "name": "ミシェル・フェアリー",
                    "character": "グレンジャー夫人",
                    "id": 99116,
                    "link": "https://filmarks.com/people/99116",
                },
                {
                    "name": "アルバン・バイラクタライ",
                    "character": "アントニン・ドロホフ",
                    "id": 67294,
                    "link": "https://filmarks.com/people/67294",
                },
                {
                    "name": "レイド・サーベジヤ",
                    "id": 92697,
                    "link": "https://filmarks.com/people/92697",
                },
                {
                    "name": "フランク・ディレイン",
                    "character": "トム・マールヴォロ・リドル",
                    "id": 79409,
                    "link": "https://filmarks.com/people/79409",
                },
                {
                    "name": "ジム・ブロードベント",
                    "character": "ホラス・スラグホーン",
                    "id": 49884,
                    "link": "https://filmarks.com/people/49884",
                },
                {
                    "name": "マイケル・ガンボン",
                    "character": "アルバス・ダンブルドア",
                    "id": 39892,
                    "link": "https://filmarks.com/people/39892",
                },
                {
                    "name": "スカーレット・バーン",
                    "character": "パンジー・パーキンソン",
                    "id": 34797,
                    "link": "https://filmarks.com/people/34797",
                },
            ],
        },
    ],
)
def test_info_with_results_single_3(client_nc, test_data, caplog) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    resp = client_nc.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert MOVIE_ENG in caplog.text

    fields = [
        "title",
        "original_title",
        "link",
        "production_year_link",
        "production_year",
        "screening_date",
        "screening_time",
        "country_of_origin",
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
    assert get_json_val(resp_data, "$.data.genre") is not None
    assert get_json_val(resp_data, "$.data.distributor") is not None
    assert get_json_val(resp_data, "$.data.creator") is not None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "グランメゾン・パリ",
            "rating": 3.8,
            "mark_count": 29379,
            "clip_count": 18394,
            "movie_id": 116998,
            "link": "https://filmarks.com/movies/116998",
            "official_site": "https://grandmaison-project.jp",
            "production_year_link": "https://filmarks.com/list/year/2020s/2024",
            "production_year": 2024,
            "screening_date": "2024年12月30日",
            "screening_time": "117分",
            "country_of_origin": [
                {
                    "name": "日本",
                    "id": 144,
                    "link": "https://filmarks.com/list/country/144",
                }
            ],
            "cast": [
                {
                    "name": "木村拓哉",
                    "character": "尾花夏樹",
                    "id": 18417,
                    "link": "https://filmarks.com/people/18417",
                },
                {
                    "name": "鈴木京香",
                    "character": "早見倫子",
                    "id": 24282,
                    "link": "https://filmarks.com/people/24282",
                },
                {
                    "name": "オク・テギョン",
                    "character": "リック・ユアン",
                    "id": 193242,
                    "link": "https://filmarks.com/people/193242",
                },
                {
                    "name": "正門良規",
                    "character": "小暮佑",
                    "id": 244456,
                    "link": "https://filmarks.com/people/244456",
                },
                {
                    "name": "玉森裕太",
                    "character": "平古祥平",
                    "id": 127408,
                    "link": "https://filmarks.com/people/127408",
                },
                {
                    "name": "寛一郎",
                    "character": "芹田公一",
                    "id": 219445,
                    "link": "https://filmarks.com/people/219445",
                },
                {
                    "name": "吉谷彩子",
                    "character": "松井萌絵",
                    "id": 17247,
                    "link": "https://filmarks.com/people/17247",
                },
                {
                    "name": "中村アン",
                    "character": "久住栞奈",
                    "id": 210512,
                    "link": "https://filmarks.com/people/210512",
                },
                {
                    "name": "冨永愛",
                    "character": "リンダ・真知子・リシャール",
                    "id": 131180,
                    "link": "https://filmarks.com/people/131180",
                },
                {
                    "name": "及川光博",
                    "character": "相沢瓶人",
                    "id": 177749,
                    "link": "https://filmarks.com/people/177749",
                },
                {
                    "name": "沢村一樹",
                    "character": "京野陸太郎",
                    "id": 126120,
                    "link": "https://filmarks.com/people/126120",
                },
            ],
        },
    ],
)
def test_info_with_results_single_4(client_nc, test_data, caplog) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    resp = client_nc.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert MOVIE_ENG in caplog.text

    fields = [
        "title",
        "link",
        "official_site",
        "production_year_link",
        "production_year",
        "screening_date",
        "screening_time",
        "country_of_origin",
        "cast",
    ]
    for field in fields:
        assert get_json_val(resp_data, f"$.data.{field}") == get_json_val(test_data, f"$.{field}")

    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.mark_count") >= get_json_val(test_data, "$.mark_count")
    assert get_json_val(resp_data, "$.data.clip_count") >= get_json_val(test_data, "$.clip_count")

    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.genre") is not None
    assert get_json_val(resp_data, "$.data.distributor") is not None
    assert get_json_val(resp_data, "$.data.creator") is None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is None


def test_info_with_results_random(client_nc, caplog) -> None:
    with open(file="tests/movie/100_movies.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        movie = choice(test_data)

    title = get_json_val(movie, "$.title")
    movie_id = get_json_val(movie, "$.id")

    resp = client_nc.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert MOVIE_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.mark_count") is not None
    assert get_json_val(resp_data, "$.data.clip_count") is not None
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert get_json_val(resp_data, "$.data.link") is not None


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "バットマン ビギンズ",
            "original_title": "Batman Begins",
            "rating": 3.8,
            "movie_id": 22767,
            "link": "https://filmarks.com/movies/22767",
            "reviews": {
                "user": {
                    "name": "shingo",
                    "id": "ZR5DnIWz",
                    "link": "https://filmarks.com/users/ZR5DnIWz",
                },
                "review": {
                    "date": "2012/08/11 12:01",
                    "rating": 3.8,
                    "id": 230,
                    "link": "https://filmarks.com/movies/22767/reviews/230",
                    "contents": "ダークナイトライジングに向けて復習。物語がバラバラしてる印象なんだけど、敵が悪としてではなくて自分たちの信じる正義を原理的に実行する人たちとして描かれてるのがよかった。",
                },
            },
        },
    ],
)
def test_review_with_results_full(client_nc, test_data, caplog) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    slug = f"movies/{movie_id}"
    last_page = get_reviews_last_page(slug)

    resp = client_nc.get(f"{slug}/reviews?page={last_page}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert MOVIE_ENG in caplog.text

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
    assert get_json_val(resp_data, "$.data.original_title") == get_json_val(test_data, "$.original_title")
    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.link") == f"{get_json_val(test_data, "$.link")}?page={last_page}"
    assert len(get_json_val(resp_data, "$.data.reviews")) > 0


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "バットマン ビギンズ",
            "rating": 3.8,
            "movie_id": 22767,
            "review_id": 230,
            "link": "https://filmarks.com/movies/22767/reviews/230",
            "review": {
                "user": {
                    "name": "shingo",
                    "id": "ZR5DnIWz",
                    "link": "https://filmarks.com/users/ZR5DnIWz",
                },
                "review": {
                    "date": "2012/08/11 12:01",
                    "rating": 3.8,
                    "contents": "ダークナイトライジングに向けて復習。物語がバラバラしてる印象なんだけど、敵が悪としてではなくて自分たちの信じる正義を原理的に実行する人たちとして描かれてるのがよかった。",
                },
            },
        },
    ],
)
def test_review_with_results_specific(client_nc, test_data, caplog) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")
    review_id = get_json_val(test_data, "$.review_id")

    resp = client_nc.get(f"movies/{movie_id}/reviews/230")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert get_json_val(resp_data, "$.data.review_id") == review_id
    assert MOVIE_ENG in caplog.text

    review_fields = [
        "user.name",
        "user.id",
        "user.link",
        "review.date",
        "review.rating",
        "review.contents"
    ]
    for field in review_fields:
        assert get_json_val(resp_data, f"$.data.review.{field}") == get_json_val(test_data, f"$.review.{field}")

    assert get_json_val(resp_data, "$.data.title") == get_json_val(test_data, "$.title")
    assert get_json_val(resp_data, "$.data.rating") == pytest.approx(get_json_val(test_data, "$.rating"), abs=0.5)
    assert get_json_val(resp_data, "$.data.link") == get_json_val(test_data, "$.link")


def test_review_with_results(client_nc, caplog) -> None:
    title = "細い目"
    original_title = "SEPET／Chinese Eyes"
    movie_id = 27402

    resp = client_nc.get(f"/movies/{movie_id}/reviews")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert MOVIE_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.original_title") == original_title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert get_json_val(resp_data, "$.data.link") is not None
    assert len(get_json_val(resp_data, "$.data.reviews")) > 0


def test_review_without_results(client_nc, caplog) -> None:
    title = "細い目"
    original_title = "SEPET／Chinese Eyes"
    movie_id = 27402

    resp = client_nc.get(f"/movies/{movie_id}/reviews?page=50")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert MOVIE_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.original_title") == original_title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert get_json_val(resp_data, "$.data.link") is not None
    assert len(get_json_val(resp_data, "$.data.reviews")) == 0


def test_review_with_results_random(client_nc, caplog) -> None:
    with open(file="tests/movie/100_movies.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        movie = choice(test_data)

    title = get_json_val(movie, "$.title")
    movie_id = get_json_val(movie, "$.id")

    resp = client_nc.get(f"/movies/{movie_id}/reviews")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert MOVIE_ENG in caplog.text
    assert get_json_val(resp_data, "$.data.title") == title
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert get_json_val(resp_data, "$.data.link") is not None
    assert len(get_json_val(resp_data, "$.data.reviews")) > 0
