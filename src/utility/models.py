from enum import Enum
from msgspec import Struct


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
        CAST = "search/people"
        USERS = "search/users"

    class InfoEP(Enum):
        DRAMAS = "dramas/{drama_series_id}/{drama_season_id}"
        CAST = "people/{person_id}"
        USERS = "users/{user_id}"

    SEARCH_ENDPOINTS = {e.value for e in SearchEP}
    INFO_ENDPOINTS = {e.value for e in InfoEP}
