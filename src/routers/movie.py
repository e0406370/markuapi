from fastapi import APIRouter, Depends, Request
from math import floor
from src.scrape.scrape_service import info_scrape, review_scrape, search_scrape
from src.utility.config import Config
from src.utility.endpoints import Endpoint
from src.utility.models import InfoResponse, ReviewParams, ListParams, SearchParams, SearchResponse
from src.utility.rediss import cache
from typing import Annotated

router = APIRouter()


@router.get("/search/movies", tags=["movie"], response_model=SearchResponse, summary="Search for movies")
@cache(expire=Config.REDIS_TTL_CACHE)
def search_movies(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.SEARCH_MOVIES,
        req=req,
        message="Failed to search movies.",
    )


@router.get("/movies/{movie_id}", tags=["movie"], response_model=InfoResponse, summary="Retrieve information about a specific movie")
@cache(expire=Config.REDIS_TTL_CACHE)
def info_movies(
    movie_id: int,
    req: Request
) -> InfoResponse:

    return info_scrape(
        endpoint=Endpoint.INFO_MOVIES,
        req=req,
        message=f"Failed to retrieve information for movie with ID: {movie_id}.",
    )


@router.get("/movies/{movie_id}/reviews", tags=["movie"], response_model=InfoResponse, summary="Retrieve user reviews about a specific movie")
@cache(expire=Config.REDIS_TTL_CACHE)
def review_movies(
    movie_id: int,
    review_params: Annotated[ReviewParams, Depends()],
    req: Request
) -> InfoResponse:

    return review_scrape(
        endpoint=Endpoint.REVIEW_MOVIES,
        req=req,
        message=f"Failed to retrieve reviews for movie with ID: {movie_id}.",
    )


@router.get("/movies/{movie_id}/reviews/{review_id}", tags=["movie"], response_model=InfoResponse, summary="Retrieve a specific user review about a specific movie")
@cache(expire=Config.REDIS_TTL_CACHE)
def review_specific_movies(
    movie_id: int,
    review_id: int,
    req: Request
) -> InfoResponse:

    return review_scrape(
        endpoint=Endpoint.REVIEW_SPECIFIC_MOVIES,
        req=req,
        message=f"Failed to retrieve review for movie with ID: {movie_id} and review ID: {review_id}.",
    )


@router.get("/list-movie/now", tags=["movie"], response_model=SearchResponse, summary="Fetch movies that are currently screening")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_currently_screening(
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_NOW,
        req=req,
        message="Failed to fetch currently screening movies.",
    )


@router.get("/list-movie/coming-soon", tags=["movie"], response_model=SearchResponse, summary="Fetch movies that are coming soon")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_coming_soon(
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_COMING,
        req=req,
        message="Failed to fetch upcoming movies.",
    )


@router.get("/list-movie/opening-this-week", tags=["movie"], response_model=SearchResponse, summary="Fetch movies that are opening this week")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_opening_this_week(
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_UPCOMING,
        req=req,
        message="Failed to fetch movies opening this week.",
    )


@router.get("/list-movie/trend", tags=["movie"], response_model=SearchResponse, summary="Fetch currently trending movies")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_trending(
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_TRENDING,
        req=req,
        message="Failed to fetch trending movies.",
    )


@router.get("/list-movie/vod/{vod_name}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies available on a specific VOD service")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_vod(
    vod_name: str,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_VOD,
        req=req,
        message=f"Failed to fetch movies from VOD service: {vod_name}.",
    )


@router.get("/list-movie/award/{award_id}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies that received a specific award")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_award(
    award_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_AWARD,
        req=req,
        message=f"Failed to fetch movies with award ID: {award_id}.",
    )


@router.get("/list-movie/year/{year_series}s", tags=["movie"], response_model=SearchResponse, summary="Fetch movies released in a specific decade")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_year_series(
    year_series: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_YEAR_SERIES,
        req=req,
        message=f"Failed to fetch movies from year series: {year_series}s.",
    )


@router.get("/list-movie/year/{year}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies released in a specific year")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_year_specific(
    year: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    req.path_params["year_series"] = floor(year / 10) * 10

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_YEAR_SPECIFIC,
        req=req,
        message=f"Failed to fetch movies from year: {year}.",
    )


@router.get("/list-movie/country/{country_id}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies from a specific country")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_country(
    country_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_COUNTRY,
        req=req,
        message=f"Failed to fetch movies with country ID: {country_id}.",
    )


@router.get("/list-movie/genre/{genre_id}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies categorised under a specific genre")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_genre(
    genre_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_GENRE,
        req=req,
        message=f"Failed to fetch movies with genre ID: {genre_id}.",
    )


@router.get("/list-movie/distributor/{distributor_id}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies associated with a specific distributor")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_distributor(
    distributor_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_DISTRIBUTOR,
        req=req,
        message=f"Failed to fetch movies with distributor ID: {distributor_id}.",
    )


@router.get("/list-movie/series/{series_id}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies categorised under a specific series")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_series(
    series_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_SERIES,
        req=req,
        message=f"Failed to fetch movies with series ID: {series_id}.",
    )


@router.get("/list-movie/tag/{tag}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies categorised under a specific tag")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_tag(
    tag: str,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_TAG,
        req=req,
        message=f"Failed to fetch movies with tag: {tag}.",
    )


@router.get("/list-movie/person/{person_id}", tags=["movie"], response_model=SearchResponse, summary="Fetch movies linked to a specific person")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_movies_person(
    person_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_MOVIES_PERSON,
        req=req,
        message=f"Failed to fetch movies with person ID: {person_id}.",
    )
