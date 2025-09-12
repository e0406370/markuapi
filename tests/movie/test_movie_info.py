from random import choice
from tests.test_utils import client, get_json_val
import json
import pytest


@pytest.mark.parametrize("path", [
    "abc"
    "８０４２",
])
def test_info_input_not_valid_integer(path) -> None:
    resp = client.get(f"/movies/{path}")
    resp_data = resp.json()

    assert resp.status_code == 422
    for err in get_json_val(resp_data, "$.detail"):
        assert get_json_val(err, "$.msg") == "Input should be a valid integer, unable to parse string as an integer"


@pytest.mark.parametrize(
    "test_data",
    [
        {
            "title": "ダークナイト",
            "original_title": "The Dark Knight",
            "rating": 4.2,
            "mark_count": 205756,
            "clip_count": 46931,
            "movie_id": 33832,
            "link": "https://filmarks.com/movies/33832",
            "production_year_link": "https://filmarks.com/list/year/2000s/2008",
            "production_year": "2008年",
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
                    "people_id": 179790,
                    "link": "https://filmarks.com/people/179790",
                },
                {
                    "name": "ヒース・レジャー",
                    "character": "ジョーカー",
                    "people_id": 96468,
                    "link": "https://filmarks.com/people/96468",
                },
                {
                    "name": "アーロン・エッカート",
                    "character": "ハービー・デント",
                    "people_id": 95575,
                    "link": "https://filmarks.com/people/95575",
                },
                {
                    "name": "マイケル・ケイン",
                    "character": "アルフレッド・ペニーワース",
                    "people_id": 129698,
                    "link": "https://filmarks.com/people/129698",
                },
                {
                    "name": "マギー・ギレンホール",
                    "character": "レイチェル・ドーズ",
                    "people_id": 76276,
                    "link": "https://filmarks.com/people/76276",
                },
                {
                    "name": "ゲイリー・オールドマン",
                    "character": "ジェームズ・“ジム”・ゴードン",
                    "people_id": 76854,
                    "link": "https://filmarks.com/people/76854",
                },
                {
                    "name": "モーガン・フリーマン",
                    "character": "ルーシャス・フォックス",
                    "people_id": 162058,
                    "link": "https://filmarks.com/people/162058",
                },
                {
                    "name": "モニーク・ガブリエラ・カーネン",
                    "character": "アンナ・ラミレス",
                    "people_id": 169378,
                    "link": "https://filmarks.com/people/169378",
                },
                {
                    "name": "ロン・ディーン",
                    "character": "マイケル・ワーツ",
                    "people_id": 168827,
                    "link": "https://filmarks.com/people/168827",
                },
                {
                    "name": "キリアン・マーフィ",
                    "character": "ジョナサン・クレイン",
                    "people_id": 32549,
                    "link": "https://filmarks.com/people/32549",
                },
                {
                    "name": "チン・ハン",
                    "character": "ラウ",
                    "people_id": 115241,
                    "link": "https://filmarks.com/people/115241",
                },
                {
                    "name": "ネスター・カーボネル",
                    "character": "アンソニー・ガルシア",
                    "people_id": 9875,
                    "link": "https://filmarks.com/people/9875",
                },
                {
                    "name": "エリック・ロバーツ",
                    "character": "サルバトーレ・マローニ",
                    "people_id": 32191,
                    "link": "https://filmarks.com/people/32191",
                },
                {
                    "name": "リッチー・コスター",
                    "character": "チェチェン人ボス",
                    "people_id": 17553,
                    "link": "https://filmarks.com/people/17553",
                },
                {
                    "name": "アンソニー・マイケル・ホール",
                    "character": "マイク・エンゲル",
                    "people_id": 157131,
                    "link": "https://filmarks.com/people/157131",
                },
                {
                    "name": "キース・ザラバッカ",
                    "character": "ジェラルド・スティーブンズ",
                    "people_id": 403,
                    "link": "https://filmarks.com/people/403",
                },
                {
                    "name": "コリン・マクファーレン",
                    "character": "ギリアン・B・ローブ",
                    "people_id": 166180,
                    "link": "https://filmarks.com/people/166180",
                },
                {
                    "name": "ジョシュア・ハート",
                    "character": "コールマン・リース",
                    "people_id": 138739,
                    "link": "https://filmarks.com/people/138739",
                },
                {
                    "name": "メリンダ・マックグロウ",
                    "character": "バーバラ・ゴードン",
                    "people_id": 118531,
                    "link": "https://filmarks.com/people/118531",
                },
                {
                    "name": "ネイサン・ギャンブル",
                    "character": "ジェームズ・“ジミー”・ゴードン・Jr",
                    "people_id": 58815,
                    "link": "https://filmarks.com/people/58815",
                },
                {
                    "name": "マイケル・ジェイ・ホワイト",
                    "character": "ギャンボル",
                    "people_id": 35406,
                    "link": "https://filmarks.com/people/35406",
                },
                {
                    "name": "ウィリアム・フィクナー",
                    "character": "銀行支店長",
                    "people_id": 4099,
                    "link": "https://filmarks.com/people/4099",
                },
                {
                    "name": "マシュー・オニール",
                    "character": "チャクルズ",
                    "people_id": 55502,
                    "link": "https://filmarks.com/people/55502",
                },
                {
                    "name": "エディソン・チャン",
                    "people_id": 74619,
                    "link": "https://filmarks.com/people/74619",
                },
                {
                    "name": "マイケル・ストヤノフ",
                    "character": "ドーピー",
                    "people_id": 159085,
                    "link": "https://filmarks.com/people/159085",
                },
                {
                    "name": "デヴィッド・ダストマルチャン",
                    "character": "トーマス・シフ",
                    "people_id": 191423,
                    "link": "https://filmarks.com/people/191423",
                },
            ],
        },
    ],
)
def test_info_with_results_single_1(test_data) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    resp = client.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id

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
    assert get_json_val(resp_data, "$.data.mark_count") == pytest.approx(get_json_val(test_data, "$.mark_count"), abs=500)
    assert get_json_val(resp_data, "$.data.clip_count") == pytest.approx(get_json_val(test_data, "$.clip_count"), abs=500)

    assert get_json_val(resp_data, "$.data.synopsis") is not None
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
            "mark_count": 55504,
            "clip_count": 13770,
            "movie_id": 69153,
            "link": "https://filmarks.com/movies/69153",
            "production_year_link": "https://filmarks.com/list/year/2010s/2017",
            "production_year": "2017年",
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
                    "people_id": 51000,
                    "link": "https://filmarks.com/people/51000",
                },
                {
                    "name": "深津絵里",
                    "character": "鈴木光恵",
                    "people_id": 143090,
                    "link": "https://filmarks.com/people/143090",
                },
                {
                    "name": "泉澤祐希",
                    "character": "鈴木賢司",
                    "people_id": 186288,
                    "link": "https://filmarks.com/people/186288",
                },
                {
                    "name": "葵わかな",
                    "character": "鈴木結衣",
                    "people_id": 192162,
                    "link": "https://filmarks.com/people/192162",
                },
                {
                    "name": "菅原大吉",
                    "people_id": 163124,
                    "link": "https://filmarks.com/people/163124",
                },
                {
                    "name": "徳井優",
                    "people_id": 90668,
                    "link": "https://filmarks.com/people/90668",
                },
                {
                    "name": "桂雀々",
                    "people_id": 136172,
                    "link": "https://filmarks.com/people/136172",
                },
                {
                    "name": "森下能幸",
                    "people_id": 35127,
                    "link": "https://filmarks.com/people/35127",
                },
                {
                    "name": "田中要次",
                    "people_id": 154675,
                    "link": "https://filmarks.com/people/154675",
                },
                {
                    "name": "有福正志",
                    "people_id": 177514,
                    "link": "https://filmarks.com/people/177514",
                },
                {
                    "name": "左時枝",
                    "people_id": 55975,
                    "link": "https://filmarks.com/people/55975",
                },
                {
                    "name": "時任三郎",
                    "character": "斎藤敏夫",
                    "people_id": 108989,
                    "link": "https://filmarks.com/people/108989",
                },
                {
                    "name": "ミッキー・カーチス",
                    "people_id": 4258,
                    "link": "https://filmarks.com/people/4258",
                },
                {
                    "name": "藤原紀香",
                    "character": "斎藤静子",
                    "people_id": 122018,
                    "link": "https://filmarks.com/people/122018",
                },
                {
                    "name": "大野拓朗",
                    "character": "斎藤涼介",
                    "people_id": 64907,
                    "link": "https://filmarks.com/people/64907",
                },
                {
                    "name": "志尊淳",
                    "character": "斎藤翔平",
                    "people_id": 194173,
                    "link": "https://filmarks.com/people/194173",
                },
                {
                    "name": "渡辺えり",
                    "character": "古田富子",
                    "people_id": 91748,
                    "link": "https://filmarks.com/people/91748",
                },
                {
                    "name": "宅麻伸",
                    "character": "高橋亮三",
                    "people_id": 126115,
                    "link": "https://filmarks.com/people/126115",
                },
                {
                    "name": "柄本明",
                    "character": "佐々木重臣",
                    "people_id": 148053,
                    "link": "https://filmarks.com/people/148053",
                },
                {
                    "name": "大地康雄",
                    "character": "田中善一",
                    "people_id": 65017,
                    "link": "https://filmarks.com/people/65017",
                },
            ],
        },
    ],
)
def test_info_with_results_single_2(test_data) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    resp = client.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id

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
    assert get_json_val(resp_data, "$.data.mark_count") == pytest.approx(get_json_val(test_data, "$.mark_count"), abs=500)
    assert get_json_val(resp_data, "$.data.clip_count") == pytest.approx(get_json_val(test_data, "$.clip_count"), abs=500)

    assert get_json_val(resp_data, "$.data.synopsis") is not None
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
            "mark_count": 211503,
            "clip_count": 12575,
            "movie_id": 27701,
            "link": "https://filmarks.com/movies/27701",
            "production_year_link": "https://filmarks.com/list/year/2010s/2010",
            "production_year": "2010年",
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
                    "people_id": 93709,
                    "link": "https://filmarks.com/people/93709",
                },
                {
                    "name": "ルパート・グリント",
                    "character": "ロン・ウィーズリー",
                    "people_id": 49543,
                    "link": "https://filmarks.com/people/49543",
                },
                {
                    "name": "エマ・ワトソン",
                    "character": "ハーマイオニー・グレンジャー",
                    "people_id": 181498,
                    "link": "https://filmarks.com/people/181498",
                },
                {
                    "name": "ヘレナ・ボナム=カーター",
                    "character": "ベラトリックス・レストレンジ",
                    "people_id": 172381,
                    "link": "https://filmarks.com/people/172381",
                },
                {
                    "name": "ロビー・コルトレーン",
                    "character": "ルビウス・ハグリッド",
                    "people_id": 133558,
                    "link": "https://filmarks.com/people/133558",
                },
                {
                    "name": "トム・フェルトン",
                    "character": "ドラコ・マルフォイ",
                    "people_id": 39284,
                    "link": "https://filmarks.com/people/39284",
                },
                {
                    "name": "レイフ・ファインズ",
                    "character": "ヴォルデモート",
                    "people_id": 53636,
                    "link": "https://filmarks.com/people/53636",
                },
                {
                    "name": "ブレンダン・グリーソン",
                    "character": "アラスター・ムーディ",
                    "people_id": 74009,
                    "link": "https://filmarks.com/people/74009",
                },
                {
                    "name": "リチャード・グリフィス",
                    "character": "バーノン・ダーズリー",
                    "people_id": 172595,
                    "link": "https://filmarks.com/people/172595",
                },
                {
                    "name": "ジョン・ハート",
                    "character": "オリバンダー老人",
                    "people_id": 141919,
                    "link": "https://filmarks.com/people/141919",
                },
                {
                    "name": "ジェイソン・アイザックス",
                    "character": "ルシウス・マルフォイ",
                    "people_id": 154590,
                    "link": "https://filmarks.com/people/154590",
                },
                {
                    "name": "ヘレン・マックロリー",
                    "character": "ナルシッサ・マルフォイ",
                    "people_id": 15531,
                    "link": "https://filmarks.com/people/15531",
                },
                {
                    "name": "ビル・ナイ",
                    "character": "ルーファス・スクリムジョール",
                    "people_id": 103981,
                    "link": "https://filmarks.com/people/103981",
                },
                {
                    "name": "ミランダ・リチャードソン",
                    "character": "リータ・スキーター",
                    "people_id": 69880,
                    "link": "https://filmarks.com/people/69880",
                },
                {
                    "name": "アラン・リックマン",
                    "character": "セブルス・スネイプ",
                    "people_id": 63940,
                    "link": "https://filmarks.com/people/63940",
                },
                {
                    "name": "ティモシー・スポール",
                    "character": "ピーター・ペティグリュー",
                    "people_id": 163849,
                    "link": "https://filmarks.com/people/163849",
                },
                {
                    "name": "イメルダ・スタウントン",
                    "character": "ドローレス・アンブリッジ",
                    "people_id": 131871,
                    "link": "https://filmarks.com/people/131871",
                },
                {
                    "name": "デヴィッド・シューリス",
                    "character": "リーマス・ルーピン",
                    "people_id": 120698,
                    "link": "https://filmarks.com/people/120698",
                },
                {
                    "name": "ジュリー・ウォルターズ",
                    "character": "モリー・ウィーズリー",
                    "people_id": 21241,
                    "link": "https://filmarks.com/people/21241",
                },
                {
                    "name": "ボニー・ライト",
                    "character": "ジニー・ウィーズリー",
                    "people_id": 56343,
                    "link": "https://filmarks.com/people/56343",
                },
                {
                    "name": "ジェームズ・フェルプス",
                    "character": "フレッド・ウィーズリー",
                    "people_id": 105900,
                    "link": "https://filmarks.com/people/105900",
                },
                {
                    "name": "オリヴァー・フェルプス",
                    "character": "ジョージ・ウィーズリー",
                    "people_id": 8433,
                    "link": "https://filmarks.com/people/8433",
                },
                {
                    "name": "サイモン・マクバーニー",
                    "character": "クリーチャー",
                    "people_id": 153912,
                    "link": "https://filmarks.com/people/153912",
                },
                {
                    "name": "ジョージ・ハリス",
                    "character": "キングズリー・シャックルボルト",
                    "people_id": 93989,
                    "link": "https://filmarks.com/people/93989",
                },
                {
                    "name": "イヴァナ・リンチ",
                    "character": "ルーナ・ラブグッド",
                    "people_id": 88775,
                    "link": "https://filmarks.com/people/88775",
                },
                {
                    "name": "マシュー・ルイス",
                    "character": "ネビル・ロングボトム",
                    "people_id": 151038,
                    "link": "https://filmarks.com/people/151038",
                },
                {
                    "name": "マーク・ウィリアムズ",
                    "character": "アーサー・ウィーズリー",
                    "people_id": 133352,
                    "link": "https://filmarks.com/people/133352",
                },
                {
                    "name": "ハリー・メリング",
                    "character": "ダドリー・ダーズリー",
                    "people_id": 154081,
                    "link": "https://filmarks.com/people/154081",
                },
                {
                    "name": "ナタリア・テナ",
                    "character": "ニンファドーラ・トンクス",
                    "people_id": 181255,
                    "link": "https://filmarks.com/people/181255",
                },
                {
                    "name": "クレマンス・ポエジー",
                    "character": "フラー・デラクール",
                    "people_id": 34868,
                    "link": "https://filmarks.com/people/34868",
                },
                {
                    "name": "デイヴ・レジーノ",
                    "people_id": 63516,
                    "link": "https://filmarks.com/people/63516",
                },
                {
                    "name": "ワーウィック・デイヴィス",
                    "people_id": 150297,
                    "link": "https://filmarks.com/people/150297",
                },
                {
                    "name": "フレディ・ストローマ",
                    "character": "コーマック・マクラーゲン",
                    "people_id": 49051,
                    "link": "https://filmarks.com/people/49051",
                },
                {
                    "name": "ピーター・マラン",
                    "character": "ヤックスリー",
                    "people_id": 1714,
                    "link": "https://filmarks.com/people/1714",
                },
                {
                    "name": "ガイ・ヘンリー",
                    "character": "パイアス・シックネス",
                    "people_id": 174548,
                    "link": "https://filmarks.com/people/174548",
                },
                {
                    "name": "ドーナル・グリーソン",
                    "character": "ビル・ウィーズリー",
                    "people_id": 144047,
                    "link": "https://filmarks.com/people/144047",
                },
                {
                    "name": "アンディ・リンデン",
                    "character": "マンダンガス・フレッチャー",
                    "people_id": 114138,
                    "link": "https://filmarks.com/people/114138",
                },
                {
                    "name": "リス・エヴァンス",
                    "character": "ゼノフィリウス・ラブグッド",
                    "people_id": 180121,
                    "link": "https://filmarks.com/people/180121",
                },
                {
                    "name": "デヴィッド・ライオール",
                    "character": "エルファイアス・ドージ",
                    "people_id": 96703,
                    "link": "https://filmarks.com/people/96703",
                },
                {
                    "name": "マッティエロック・ギブス",
                    "character": "ミュリエル・プルウェット",
                    "people_id": 108040,
                    "link": "https://filmarks.com/people/108040",
                },
                {
                    "name": "ニック・モラン",
                    "character": "スカビオール",
                    "people_id": 70470,
                    "link": "https://filmarks.com/people/70470",
                },
                {
                    "name": "ジェイミー・キャンベル・バウアー",
                    "character": "ゲラート・グリンデルバルド",
                    "people_id": 81369,
                    "link": "https://filmarks.com/people/81369",
                },
                {
                    "name": "キャロライン・ピクルズ",
                    "people_id": 91214,
                    "link": "https://filmarks.com/people/91214",
                },
                {
                    "name": "ミシェル・フェアリー",
                    "character": "グレンジャー夫人",
                    "people_id": 99116,
                    "link": "https://filmarks.com/people/99116",
                },
                {
                    "name": "アルバン・バイラクタライ",
                    "character": "アントニン・ドロホフ",
                    "people_id": 67294,
                    "link": "https://filmarks.com/people/67294",
                },
                {
                    "name": "レイド・サーベジヤ",
                    "people_id": 92697,
                    "link": "https://filmarks.com/people/92697",
                },
                {
                    "name": "フランク・ディレイン",
                    "character": "トム・マールヴォロ・リドル",
                    "people_id": 79409,
                    "link": "https://filmarks.com/people/79409",
                },
                {
                    "name": "ジム・ブロードベント",
                    "character": "ホラス・スラグホーン",
                    "people_id": 49884,
                    "link": "https://filmarks.com/people/49884",
                },
                {
                    "name": "マイケル・ガンボン",
                    "character": "アルバス・ダンブルドア",
                    "people_id": 39892,
                    "link": "https://filmarks.com/people/39892",
                },
                {
                    "name": "スカーレット・バーン",
                    "character": "パンジー・パーキンソン",
                    "people_id": 34797,
                    "link": "https://filmarks.com/people/34797",
                },
            ],
        },
    ],
)
def test_info_with_results_single_3(test_data) -> None:
    movie_id = get_json_val(test_data, "$.movie_id")

    resp = client.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id

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
    assert get_json_val(resp_data, "$.data.mark_count") == pytest.approx(get_json_val(test_data, "$.mark_count"), abs=500)
    assert get_json_val(resp_data, "$.data.clip_count") == pytest.approx(get_json_val(test_data, "$.clip_count"), abs=500)

    assert get_json_val(resp_data, "$.data.synopsis") is not None
    assert get_json_val(resp_data, "$.data.poster") is not None
    assert get_json_val(resp_data, "$.data.genre") is not None
    assert get_json_val(resp_data, "$.data.distributor") is not None
    assert get_json_val(resp_data, "$.data.creator") is not None
    assert get_json_val(resp_data, "$.data.director") is not None
    assert get_json_val(resp_data, "$.data.scriptwriter") is not None
    assert get_json_val(resp_data, "$.data.artist") is None


def test_info_with_results_random() -> None:
    with open(file="tests/movie/100_movies.json", mode="r", encoding="utf-8") as f:
        test_data = json.load(f)
        movie = choice(test_data)

    movie_id = get_json_val(movie, "$.id")

    resp = client.get(f"/movies/{movie_id}")
    resp_data = resp.json()

    assert resp.status_code == 200
    assert get_json_val(resp_data, "$.data.title") is not None
    assert get_json_val(resp_data, "$.data.rating") is not None
    assert get_json_val(resp_data, "$.data.mark_count") is not None
    assert get_json_val(resp_data, "$.data.clip_count") is not None
    assert get_json_val(resp_data, "$.data.movie_id") == movie_id
    assert get_json_val(resp_data, "$.data.link") is not None
    assert get_json_val(resp_data, "$.data.production_year_link") is not None
    assert get_json_val(resp_data, "$.data.production_year") is not None
