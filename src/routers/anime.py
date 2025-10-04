from fastapi import APIRouter, Depends, Request
from math import floor
from src.scrape.scrape_service import info_scrape, review_scrape, search_scrape
from src.utility.config import Config
from src.utility.endpoints import Endpoint
from src.utility.models import InfoResponse, ReviewParams, ListParams, SearchParams, SearchResponse
from src.utility.rediss import cache
from typing import Annotated

router = APIRouter()


@router.get("/search/animes", tags=["anime"], response_model=SearchResponse, summary="Search for animes")
@cache(expire=Config.REDIS_TTL_CACHE)
def search_animes(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.SEARCH_ANIMES,
        req=req,
        message="Failed to search animes.",
    )


@router.get("/animes/{anime_series_id}/{anime_season_id}", tags=["anime"], response_model=InfoResponse, summary="Retrieve information about a specific anime")
@cache(expire=Config.REDIS_TTL_CACHE)
def info_animes(
    anime_series_id: int,
    anime_season_id: int,
    req: Request
) -> InfoResponse:

    return info_scrape(
        endpoint=Endpoint.INFO_ANIMES,
        req=req,
        message=f"Failed to retrieve information for anime with series ID: {anime_series_id} and season ID: {anime_season_id}.",
    )


@router.get("/animes/{anime_series_id}/{anime_season_id}/reviews", tags=["anime"], response_model=InfoResponse, summary="Retrieve user reviews about a specific anime")
@cache(expire=Config.REDIS_TTL_CACHE)
def review_animes(
    anime_series_id: int,
    anime_season_id: int,
    review_params: Annotated[ReviewParams, Depends()],
    req: Request
) -> InfoResponse:

    return review_scrape(
        endpoint=Endpoint.REVIEW_ANIMES,
        req=req,
        message=f"Failed to retrieve reviews for anime with series ID: {anime_series_id} and season ID: {anime_season_id}.",
    )


@router.get("/list-anime/trend", tags=["anime"], response_model=SearchResponse, summary="Fetch currently trending animes")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_trending(
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_TRENDING,
        req=req,
        message="Failed to fetch trending animes.",
    )


@router.get("/list-anime/vod/{vod_name}", tags=["anime"], response_model=SearchResponse, summary="Fetch animes available on a specific VOD service")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_vod(
    vod_name: str,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_VOD,
        req=req,
        message=f"Failed to fetch animes from VOD service: {vod_name}.",
    )


@router.get("/list-anime/year/{year_series}s", tags=["anime"], response_model=SearchResponse, summary="Fetch animes released in a specific decade")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_year_series(
    year_series: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_YEAR_SERIES,
        req=req,
        message=f"Failed to fetch animes from year series: {year_series}s.",
    )


@router.get("/list-anime/year/{year}", tags=["anime"], response_model=SearchResponse, summary="Fetch animes released in a specific year")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_year_specific(
    year: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    req.path_params["year_series"] = floor(year / 10) * 10

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_YEAR_SPECIFIC,
        req=req,
        message=f"Failed to fetch animes from year: {year}.",
    )


@router.get("/list-anime/year/{year}/{season_id}", tags=["anime"], response_model=SearchResponse, summary="Fetch animes released in a specific year and season")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_year_season(
    year: int,
    season_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_YEAR_SEASON,
        req=req,
        message=f"Failed to fetch animes from year: {year} with season ID: {season_id}.",
    )


@router.get("/list-anime/company/{company_id}", tags=["anime"], response_model=SearchResponse, summary="Fetch animes associated with a specific production company")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_company(
    company_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_COMPANY,
        req=req,
        message=f"Failed to fetch animes with company ID: {company_id}.",
    )


@router.get("/list-anime/tag/{tag}", tags=["anime"], response_model=SearchResponse, summary="Fetch animes categorised under a specific tag")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_tag(
    tag: str,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_TAG,
        req=req,
        message=f"Failed to fetch animes with tag: {tag}.",
    )


@router.get("/list-anime/person/{person_id}", tags=["anime"], response_model=SearchResponse, summary="Fetch animes linked to a specific person")
@cache(expire=Config.REDIS_TTL_CACHE)
def list_animes_person(
    person_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_PERSON,
        req=req,
        message=f"Failed to fetch animes with person ID: {person_id}.",
    )
