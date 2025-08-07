from enum import Enum
from msgspec import Struct
from pydantic import BaseModel, Field
from typing import Dict
from urllib.parse import urljoin


class DataClip(Struct):
    drama_series_id: int
    drama_season_id: int
    count: int


class DataMark(Struct):
    drama_series_id: int
    drama_season_id: int
    count: int


class Filmarks:
    FILMARKS_BASE = "https://filmarks.com/"

    class SearchEP(Enum):
        DRAMAS = "search/dramas"
        DRAMAS_TRENDING = "list-drama/trend"

        CAST = "search/people"
        USERS = "search/users"

    class InfoEP(Enum):
        DRAMAS = "dramas/{drama_series_id}/{drama_season_id}"

        CAST = "people/{person_id}"
        USERS = "users/{user_id}"

    SEARCH_ENDPOINTS = {e.value for e in SearchEP}
    INFO_ENDPOINTS = {e.value for e in InfoEP}

    @staticmethod
    def create_filmarks_link(url: str) -> str:
        return urljoin(base=Filmarks.FILMARKS_BASE, url=url)

    @staticmethod
    def create_person_info(name: str, link: str, character: str = "") -> Dict[str, str]:
        person_info = {}

        person_info["name"] = name
        if character: person_info["character"] = character

        link = Filmarks.create_filmarks_link(link)
        person_info["people_id"] = int(link.split("people/")[1])
        person_info["link"] = link

        return person_info


class SearchParams(BaseModel):
    limit: int = Field(10, gt=0, le=1000)
    page: int = Field(1, gt=0, le=1000)
