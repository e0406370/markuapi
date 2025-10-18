from datetime import datetime, timezone
from enum import Enum
from msgspec import Struct
from src.utility.models import AnimeDataClip, AnimeDataMark, DramaDataClip, DramaDataMark, MovieDataClip, MovieDataMark
from typing import Any, Dict, Set, Tuple
from urllib.parse import urljoin


class EndpointType(str, Enum):
    PATH = "path"
    QUERY = "query"
    COMBINED = "path+query"


class ViewType(str, Enum):
    ANIME = "anime"
    DRAMA = "drama"
    MOVIE = "movie"

    @property
    def mark(self) -> Struct:
        marks: Dict[ViewType, Struct] = {
            ViewType.ANIME: AnimeDataMark,
            ViewType.DRAMA: DramaDataMark,
            ViewType.MOVIE: MovieDataMark,
        }

        return marks[self]

    @property
    def clip(self) -> Struct:
        clips: Dict[ViewType, Struct] = {
            ViewType.ANIME: AnimeDataClip,
            ViewType.DRAMA: DramaDataClip,
            ViewType.MOVIE: MovieDataClip,
        }
        
        return clips[self]


class OtherInfo(Tuple[str, str], Enum):
    RELEASE_DATE = ("release_date", "公開日：")
    SCREENING_DATE = ("screening_date", "上映日：")
    PLAYBACK_TIME = ("playback_time", "再生時間：")
    SCREENING_TIME = ("screening_time", "上映時間：")
    COUNTRY_OF_ORIGIN = ("country_of_origin", "製作国・地域：")
    PRODUCTION_COMPANY = ("production_company", "制作会社：")
    GENRE = ("genre", "ジャンル：")
    DISTRIBUTOR = ("distributor", "配給：")

    @property
    def key(self) -> str:
        return self.value[0]

    @property
    def title(self) -> str:
        return self.value[1]

    @classmethod
    def single_fields(cls) -> Set[Tuple[str, str]]:
        return {
            cls.RELEASE_DATE,
            cls.SCREENING_DATE,
            cls.PLAYBACK_TIME,
            cls.SCREENING_TIME,
        }


class PersonInfo(Tuple[str, str], Enum):
    CREATOR = ("creator", "原作")
    PLANNER = ("planner", "企画")
    PRODUCER_1 = ("producer", "制作")
    PRODUCER_2 = ("producer", "製作")
    EXECUTIVE_PRODUCER_1 = ("executive_producer", "制作総指揮")
    EXECUTIVE_PRODUCER_2 = ("executive_producer", "製作総指揮")
    CHIEF_DIRECTOR = ("chief_director", "総監督")
    DIRECTOR = ("director", "監督")
    SERIES_COMPOSER = ("series_composer", "シリーズ構成")
    SCRIPTWRITER = ("scriptwriter", "脚本")
    CHARACTER_ORIGINAL_DESIGNER = ("character_original_designer", "キャラクター原案")
    CHARACTER_DESIGNER = ("character_designer", "キャラクターデザイン")
    NARRATOR = ("narrator", "ナレーション")
    ARTIST = ("artist", "主題歌／挿入歌")
    CAST = ("cast", "出演者")

    @property
    def key(self) -> str:
        return self.value[0]

    @property
    def title(self) -> str:
        return self.value[1]


class Utils:
    FILMARKS_BASE = "https://filmarks.com/"
    FILMARKS_REQUEST_HEADERS = {
        "Referer": FILMARKS_BASE,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    }

    @staticmethod
    def get_scrape_date() -> datetime:
        return datetime.now(timezone.utc).isoformat(sep=" ", timespec="microseconds")

    @staticmethod
    def create_filmarks_link(url: str) -> str:
        return urljoin(base=Utils.FILMARKS_BASE, url=url)

    @staticmethod
    def create_other_info(name: str, link: str) -> Dict[str, Any]:
        other_info = {}

        other_info["name"] = name
        other_info["id"] = int(link.split("/")[-1])
        other_info["link"] = Utils.create_filmarks_link(link)

        return other_info

    @staticmethod
    def create_person_info(name: str, link: str, character: str = "") -> Dict[str, Any]:
        person_info = {}

        person_info["name"] = name
        if character:
            person_info["character"] = character
        person_info["id"] = int(link.split("/")[-1])
        person_info["link"] = Utils.create_filmarks_link(link)

        return person_info

    @staticmethod
    def create_review_info(user_name: str, user_link: str, review_date: str, review_rating: str, review_contents: str = "", review_link: str = "") -> Dict[str, Any]:
        review_info = {}

        user = {}
        user["name"] = user_name
        user["id"] = user_link.split("/")[-1]
        user["link"] = Utils.create_filmarks_link(user_link)
        review_info["user"] = user

        review = {}
        review["date"] = review_date
        review["rating"] = review_rating
        if review_contents:
            review["contents"] = review_contents
        if review_link:
            review["id"] = int(review_link.split("/")[-1])
            review["link"] = Utils.create_filmarks_link(review_link)
        review_info["review"] = review

        return review_info
