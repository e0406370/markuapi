from enum import Enum
from pydantic import TypeAdapter, ValidationError
from src.utility.models import Endpoint
from src.utility.utils import Constants
from typing import Dict, override


class Endpoints(Enum):
    SEARCH_ANIMES: Dict[str, str] = {
        "path": "search/animes",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_ANIME,
    }

    INFO_ANIMES: Dict[str, str] = {
        "path": "animes/{anime_series_id}/{anime_season_id}",
        "type": Constants.TYPE_PATH,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_TRENDING: Dict[str, str] = {
        "path": "list-anime/trend",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_VOD: Dict[str, str] = {
        "path": "list-anime/vod/{vod_name}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_YEAR_SERIES: Dict[str, str] = {
        "path": "list-anime/year/{year_series}s",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_YEAR_SPECIFIC: Dict[str, str] = {
        "path": "list-anime/year/{year_series}s/{year}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_YEAR_SEASON: Dict[str, str] = {
        "path": "list-anime/release_year/{year}/{season_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_COMPANY: Dict[str, str] = {
        "path": "list-anime/company/{company_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_TAG: Dict[str, str] = {
        "path": "list-anime/tag/{tag}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_ANIME,
    }

    LIST_ANIMES_PERSON: Dict[str, str] = {
        "path": "people/{person_id}/animes",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_ANIME,
    }

    SEARCH_DRAMAS: Dict[str, str] = {
        "path": "search/dramas",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_DRAMA,
    }

    INFO_DRAMAS: Dict[str, str] = {
        "path": "dramas/{drama_series_id}/{drama_season_id}",
        "type": Constants.TYPE_PATH,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_TRENDING: Dict[str, str] = {
        "path": "list-drama/trend",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_VOD: Dict[str, str] = {
        "path": "list-drama/vod/{vod_name}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_YEAR_SERIES: Dict[str, str] = {
        "path": "list-drama/year/{year_series}s",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_YEAR_SPECIFIC: Dict[str, str] = {
        "path": "list-drama/year/{year_series}s/{year}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_COUNTRY: Dict[str, str] = {
        "path": "list-drama/country/{country_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_GENRE: Dict[str, str] = {
        "path": "list-drama/genre/{genre_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_TAG: Dict[str, str] = {
        "path": "list-drama/tag/{tag}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_DRAMA,
    }

    LIST_DRAMAS_PERSON: Dict[str, str] = {
        "path": "people/{person_id}/dramas",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_DRAMA,
    }

    SEARCH_MOVIES: Dict[str, str] = {
        "path": "search/movies",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_MOVIE,
    }

    INFO_MOVIES: Dict[str, str] = {
        "path": "movies/{movie_id}",
        "type": Constants.TYPE_PATH,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_NOW: Dict[str, str] = {
        "path": "list/now",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_COMING: Dict[str, str] = {
        "path": "list/coming",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_UPCOMING: Dict[str, str] = {
        "path": "list/upcoming",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_TRENDING: Dict[str, str] = {
        "path": "list/trend",
        "type": Constants.TYPE_QUERY,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_VOD: Dict[str, str] = {
        "path": "list/vod/{vod_name}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_AWARD: Dict[str, str] = {
        "path": "list/award/{award_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_YEAR_SERIES: Dict[str, str] = {
        "path": "list/year/{year_series}s",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_YEAR_SPECIFIC: Dict[str, str] = {
        "path": "list/year/{year_series}s/{year}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_COUNTRY: Dict[str, str] = {
        "path": "list/country/{country_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_GENRE: Dict[str, str] = {
        "path": "list/genre/{genre_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_DISTRIBUTOR: Dict[str, str] = {
        "path": "list/distributor/{distributor_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_SERIES: Dict[str, str] = {
        "path": "list/series/{series_id}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_TAG: Dict[str, str] = {
        "path": "list/tag/{tag}",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    LIST_MOVIES_PERSON: Dict[str, str] = {
        "path": "people/{person_id}/movies",
        "type": Constants.TYPE_COMBINED,
        "view": Constants.VIEW_MOVIE,
    }

    @override
    def __new__(cls, endpoint: Dict[str, str]) -> object:
        ta = TypeAdapter(Endpoint)

        try:
            ta.validate_python(endpoint)

            obj = object.__new__(cls)
            obj._value_ = endpoint
            return obj

        except ValidationError as e:
            raise ValueError(e)
