from fastapi import APIRouter, Depends, Request
from math import floor
from src.scrape.scrape_service import info_scrape, search_scrape
from src.utility.endpoints import Endpoints
from src.utility.models import SearchParams
from typing import Annotated, Any, Dict

router = APIRouter()


@router.get("/search/movies")
def search_movies(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.SEARCH_MOVIES.value,
        req=req,
        message="Failed to search movies.",
    )


@router.get("/movies/{movie_id}")
def info_movies(
    movie_id: int,
    req: Request
) -> Dict[str, Any]:

    return info_scrape(
        endpoint=Endpoints.INFO_MOVIES.value,
        req=req,
        message=f"Failed to retrieve movie information with ID: {movie_id}.",
    )


@router.get("/list-movie/now")
def list_movies_currently_screening(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_NOW.value,
        req=req,
        message="Failed to fetch currently screening movies.",
    )


@router.get("/list-movie/coming-soon")
def list_movies_coming_soon(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_COMING.value,
        req=req,
        message="Failed to fetch upcoming movies.",
    )


@router.get("/list-movie/opening-this-week")
def list_movies_opening_this_week(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_UPCOMING.value,
        req=req,
        message="Failed to fetch movies opening this week.",
    )


@router.get("/list-movie/trend")
def list_movies_trending(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_TRENDING.value,
        req=req,
        message="Failed to fetch trending movies.",
    )


@router.get("/list-movie/vod/{vod_name}")
def list_movies_vod(
    vod_name: str,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_VOD.value,
        req=req,
        message=f"Failed to fetch movies from VOD service: {vod_name}.",
    )


@router.get("/list-movie/award/{award_id}")
def list_movies_award(
    award_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_AWARD.value,
        req=req,
        message=f"Failed to fetch movies with award ID: {award_id}.",
    )


@router.get("/list-movie/year/{year_series}s")
def list_movies_year_series(
    year_series: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_YEAR_SERIES.value,
        req=req,
        message=f"Failed to fetch movies from year series: {year_series}s.",
    )


@router.get("/list-movie/year/{year}")
def list_movies_year_specific(
    year: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    req.path_params["year_series"] = floor(year / 10) * 10

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_YEAR_SPECIFIC.value,
        req=req,
        message=f"Failed to fetch movies from year: {year}.",
    )


@router.get("/list-movie/country/{country_id}")
def list_movies_country(
    country_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_COUNTRY.value,
        req=req,
        message=f"Failed to fetch movies with country ID: {country_id}.",
    )


@router.get("/list-movie/genre/{genre_id}")
def list_movies_genre(
    genre_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_GENRE.value,
        req=req,
        message=f"Failed to fetch movies with genre ID: {genre_id}.",
    )


@router.get("/list-movie/distributor/{distributor_id}")
def list_movies_distributor(
    distributor_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_DISTRIBUTOR.value,
        req=req,
        message=f"Failed to fetch movies with distributor ID: {distributor_id}.",
    )


@router.get("/list-movie/series/{series_id}")
def list_movies_series(
    series_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_SERIES.value,
        req=req,
        message=f"Failed to fetch movies with series ID: {series_id}.",
    )


@router.get("/list-movie/tag/{tag}")
def list_movies_tag(
    tag: str,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_TAG.value,
        req=req,
        message=f"Failed to fetch movies with tag: {tag}.",
    )


@router.get("/list-movie/person/{person_id}")
def list_movies_person(
    person_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoints.LIST_MOVIES_PERSON.value,
        req=req,
        message=f"Failed to fetch movies with person ID: {person_id}.",
    )
