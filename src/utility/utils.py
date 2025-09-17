from datetime import datetime, timezone
from msgspec import Struct
from src.utility.models import AnimeDataClip, AnimeDataMark, DramaDataClip, DramaDataMark, MovieDataClip, MovieDataMark
from typing import Dict, Set, Tuple
from urllib.parse import urljoin


class Constants:
    FILMARKS_BASE = "https://filmarks.com/"

    TYPE_PATH = "path"
    TYPE_QUERY = "query"
    TYPE_COMBINED = "path+query"
    TYPES: Set[str] = {
        TYPE_PATH,
        TYPE_QUERY,
        TYPE_COMBINED,
    }

    VIEW_ANIME = "anime"
    VIEW_DRAMA = "drama"
    VIEW_MOVIE = "movie"
    VIEWS: Set[str] = {
        VIEW_ANIME,
        VIEW_DRAMA,
        VIEW_MOVIE,
    }
    MARKS: Dict[str, Struct] = {
        VIEW_ANIME: AnimeDataMark,
        VIEW_DRAMA: DramaDataMark,
        VIEW_MOVIE: MovieDataMark,
    }
    CLIPS: Dict[str, Struct] = {
        VIEW_ANIME: AnimeDataClip,
        VIEW_DRAMA: DramaDataClip,
        VIEW_MOVIE: MovieDataClip,
    }

    OTHER_INFO_RELEASE_DATE = ("release_date", "公開日：")
    OTHER_INFO_SCREENING_DATE = ("screening_date", "上映日：")
    OTHER_INFO_PLAYBACK_TIME = ("playback_time", "再生時間：")
    OTHER_INFO_SCREENING_TIME = ("screening_time", "上映時間：")
    OTHER_INFO_COUNTRY_OF_ORIGIN = ("country_of_origin", "製作国・地域：")
    OTHER_INFO_PRODUCTION_COMPANY = ("production_company", "制作会社：")
    OTHER_INFO_GENRE = ("genre", "ジャンル：")
    OTHER_INFO_DISTRIBUTOR = ("distributor", "配給：")
    OTHER_INFO: Set[Tuple[str, str]] = {
        OTHER_INFO_RELEASE_DATE,
        OTHER_INFO_SCREENING_DATE,
        OTHER_INFO_PLAYBACK_TIME,
        OTHER_INFO_SCREENING_TIME,
        OTHER_INFO_COUNTRY_OF_ORIGIN,
        OTHER_INFO_PRODUCTION_COMPANY,
        OTHER_INFO_GENRE,
        OTHER_INFO_DISTRIBUTOR,
    }
    OTHER_INFO_SINGLE: Set[Tuple[str, str]] = {
        OTHER_INFO_RELEASE_DATE,
        OTHER_INFO_SCREENING_DATE,
        OTHER_INFO_PLAYBACK_TIME,
        OTHER_INFO_SCREENING_TIME,
    }

    PERSON_INFO_CREATOR = ("creator", "原作")
    PERSON_INFO_PLANNER = ("planner", "企画")
    PERSON_INFO_PRODUCER_1 = ("producer", "制作")
    PERSON_INFO_PRODUCER_2 = ("producer", "製作")
    PERSON_INFO_EXECUTIVE_PRODUCER_1 = ("executive_producer", "制作総指揮")
    PERSON_INFO_EXECUTIVE_PRODUCER_2 = ("executive_producer", "製作総指揮")
    PERSON_INFO_CHIEF_DIRECTOR = ("chief_director", "総監督")
    PERSON_INFO_DIRECTOR = ("director", "監督")
    PERSON_INFO_SERIES_COMPOSER = ("series_composer", "シリーズ構成")
    PERSON_INFO_SCRIPTWRITER = ("scriptwriter", "脚本")
    PERSON_INFO_CHARACTER_ORIGINAL_DESIGNER = ("character_original_designer", "キャラクター原案")
    PERSON_INFO_CHARACTER_DESIGNER = ("character_designer", "キャラクターデザイン")
    PERSON_INFO_NARRATOR = ("narrator", "ナレーション")
    PERSON_INFO_ARTIST = ("artist", "主題歌／挿入歌")
    PERSON_INFO_CAST = ("cast", "出演者")
    PERSON_INFO: Set[Tuple[str, str]] = {
        PERSON_INFO_CREATOR,
        PERSON_INFO_PLANNER,
        PERSON_INFO_PRODUCER_1,
        PERSON_INFO_PRODUCER_2,
        PERSON_INFO_EXECUTIVE_PRODUCER_1,
        PERSON_INFO_EXECUTIVE_PRODUCER_2,
        PERSON_INFO_CHIEF_DIRECTOR,
        PERSON_INFO_DIRECTOR,
        PERSON_INFO_SERIES_COMPOSER,
        PERSON_INFO_SCRIPTWRITER,
        PERSON_INFO_CHARACTER_ORIGINAL_DESIGNER,
        PERSON_INFO_CHARACTER_DESIGNER,
        PERSON_INFO_NARRATOR,
        PERSON_INFO_ARTIST,
        PERSON_INFO_CAST,
    }


class Utils:
    @staticmethod
    def raise_value_error(item: str, group: Set) -> None:
        options = ", ".join(f"'{i}'" for i in group)
        raise ValueError(f"'{item}' can only be one of these: {options}")

    @staticmethod
    def get_scrape_date() -> datetime:
        return datetime.now(timezone.utc).isoformat(sep=" ", timespec="seconds")

    @staticmethod
    def create_filmarks_link(url: str) -> str:
        return urljoin(base=Constants.FILMARKS_BASE, url=url)

    @staticmethod
    def create_other_info(name: str, link: str) -> Dict[str, str]:
        other_info = {}

        other_info["name"] = name

        other_info["id"] = int(link.split("/")[-1])
        other_info["link"] = Utils.create_filmarks_link(link)

        return other_info

    @staticmethod
    def create_person_info(name: str, link: str, character: str = "") -> Dict[str, str]:
        person_info = {}

        person_info["name"] = name
        if character: person_info["character"] = character

        person_info["id"] = int(link.split("/")[-1])
        person_info["link"] = Utils.create_filmarks_link(link)

        return person_info

    @staticmethod
    def create_review_info(user_name: str, user_link: str, review_date: str, review_rating: str, review_link: str, review_contents: str) -> Dict[str, str]:
        review_info = {}

        user = {}
        user["name"] = user_name
        user["id"] = user_link.split("/")[-1]
        user["link"] = Utils.create_filmarks_link(user_link)
        review_info["user"] = user

        review = {}
        review["date"] = review_date
        review["rating"] = review_rating
        review["id"] = int(review_link.split("/")[-1])
        review["link"] = Utils.create_filmarks_link(review_link)
        if review_contents: review["contents"] = review_contents
        review_info["review"] = review

        return review_info
