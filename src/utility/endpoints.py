from enum import Enum
from pydantic import BaseModel
from src.utility.utils import EndpointType, ViewType


class EndpointModel(BaseModel):
    path: str
    type: EndpointType
    view: ViewType


class Endpoint(Enum):
    SEARCH_ANIMES = EndpointModel(
        path="search/animes",
        type=EndpointType.QUERY,
        view=ViewType.ANIME
    )

    INFO_ANIMES = EndpointModel(
        path="animes/{anime_series_id}/{anime_season_id}",
        type=EndpointType.PATH,
        view=ViewType.ANIME
    )

    REVIEW_ANIMES = EndpointModel(
        path="animes/{anime_series_id}/{anime_season_id}",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    LIST_ANIMES_TRENDING = EndpointModel(
        path="list-anime/trend",
        type=EndpointType.QUERY,
        view=ViewType.ANIME
    )

    LIST_ANIMES_VOD = EndpointModel(
        path="list-anime/vod/{vod_name}",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    LIST_ANIMES_YEAR_SERIES = EndpointModel(
        path="list-anime/year/{year_series}s",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    LIST_ANIMES_YEAR_SPECIFIC = EndpointModel(
        path="list-anime/year/{year_series}s/{year}",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    LIST_ANIMES_YEAR_SEASON = EndpointModel(
        path="list-anime/release_year/{year}/{season_id}",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    LIST_ANIMES_COMPANY = EndpointModel(
        path="list-anime/company/{company_id}",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    LIST_ANIMES_TAG = EndpointModel(
        path="list-anime/tag/{tag}",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    LIST_ANIMES_PERSON = EndpointModel(
        path="people/{person_id}/animes",
        type=EndpointType.COMBINED,
        view=ViewType.ANIME
    )

    SEARCH_DRAMAS = EndpointModel(
        path="search/dramas",
        type=EndpointType.QUERY,
        view=ViewType.DRAMA
    )

    INFO_DRAMAS = EndpointModel(
        path="dramas/{drama_series_id}/{drama_season_id}",
        type=EndpointType.PATH,
        view=ViewType.DRAMA
    )

    REVIEW_DRAMAS = EndpointModel(
        path="dramas/{drama_series_id}/{drama_season_id}",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_TRENDING = EndpointModel(
        path="list-drama/trend",
        type=EndpointType.QUERY,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_VOD = EndpointModel(
        path="list-drama/vod/{vod_name}",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_YEAR_SERIES = EndpointModel(
        path="list-drama/year/{year_series}s",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_YEAR_SPECIFIC = EndpointModel(
        path="list-drama/year/{year_series}s/{year}",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_COUNTRY = EndpointModel(
        path="list-drama/country/{country_id}",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_GENRE = EndpointModel(
        path="list-drama/genre/{genre_id}",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_TAG = EndpointModel(
        path="list-drama/tag/{tag}",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    LIST_DRAMAS_PERSON = EndpointModel(
        path="people/{person_id}/dramas",
        type=EndpointType.COMBINED,
        view=ViewType.DRAMA
    )

    SEARCH_MOVIES = EndpointModel(
        path="search/movies",
        type=EndpointType.QUERY,
        view=ViewType.MOVIE
    )

    INFO_MOVIES = EndpointModel(
        path="movies/{movie_id}",
        type=EndpointType.PATH,
        view=ViewType.MOVIE
    )

    REVIEW_MOVIES = EndpointModel(
        path="movies/{movie_id}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_NOW = EndpointModel(
        path="list/now",
        type=EndpointType.QUERY,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_COMING = EndpointModel(
        path="list/coming",
        type=EndpointType.QUERY,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_UPCOMING = EndpointModel(
        path="list/upcoming",
        type=EndpointType.QUERY,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_TRENDING = EndpointModel(
        path="list/trend",
        type=EndpointType.QUERY,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_VOD = EndpointModel(
        path="list/vod/{vod_name}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_AWARD = EndpointModel(
        path="list/award/{award_id}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_YEAR_SERIES = EndpointModel(
        path="list/year/{year_series}s",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_YEAR_SPECIFIC = EndpointModel(
        path="list/year/{year_series}s/{year}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_COUNTRY = EndpointModel(
        path="list/country/{country_id}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_GENRE = EndpointModel(
        path="list/genre/{genre_id}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_DISTRIBUTOR = EndpointModel(
        path="list/distributor/{distributor_id}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_SERIES = EndpointModel(
        path="list/series/{series_id}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_TAG = EndpointModel(
        path="list/tag/{tag}",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )

    LIST_MOVIES_PERSON = EndpointModel(
        path="people/{person_id}/movies",
        type=EndpointType.COMBINED,
        view=ViewType.MOVIE
    )
