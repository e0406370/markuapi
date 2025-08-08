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

    class Endpoints(Enum):
        SEARCH_DRAMAS: Dict[str, str] = {
            "path": "search/dramas",
            "type": "query",
        }

        SEARCH_CAST: Dict[str, str] = {
            "path": "search/people",
            "type": "query",
        }
 
        SEARCH_USERS: Dict[str, str] = {
            "path": "search/users",
            "type": "query",
        }

        INFO_DRAMAS: Dict[str, str] = {
            "path": "dramas/{drama_series_id}/{drama_season_id}",
            "type": "path",
        }

        INFO_CAST: Dict[str, str] = {
            "path": "people/{person_id}",
            "type": "path",
        }

        INFO_USERS: Dict[str, str] = {
            "path": "users/{user_id}",
            "type": "path",
        }

        LIST_DRAMAS_COUNTRY: Dict[str, str] = {
            "path": "list-drama/country/{country_id}",
            "type": "path+query",
        }

        LIST_DRAMAS_TRENDING: Dict[str, str] = {
            "path": "list-drama/trend",
            "type": "query",
        }

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
