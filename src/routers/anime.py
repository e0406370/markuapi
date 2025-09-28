from fastapi import APIRouter, Depends, Request
from math import floor
from src.scrape.scrape_service import info_scrape, review_scrape, search_scrape
from src.utility.endpoints import Endpoint
from src.utility.models import ReviewParams, SearchParams
from typing import Annotated, Any, Dict

router = APIRouter()


@router.get("/search/animes")
def search_animes(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.SEARCH_ANIMES,
        req=req,
        message="Failed to search animes.",
    )


@router.get("/animes/{anime_series_id}/{anime_season_id}")
def info_animes(
    anime_series_id: int,
    anime_season_id: int,
    req: Request
) -> Dict[str, Any]:

    return info_scrape(
        endpoint=Endpoint.INFO_ANIMES,
        req=req,
        message=f"Failed to retrieve information for anime with series ID: {anime_series_id} and season ID: {anime_season_id}.",
    )


@router.get("/animes/{anime_series_id}/{anime_season_id}/reviews")
def review_animes(
    anime_series_id: int,
    anime_season_id: int,
    review_params: Annotated[ReviewParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return review_scrape(
        endpoint=Endpoint.REVIEW_ANIMES,
        req=req,
        message=f"Failed to retrieve reviews for anime with series ID: {anime_series_id} and season ID: {anime_season_id}.",
    )


@router.get("/list-anime/trend")
def list_animes_trending(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_TRENDING,
        req=req,
        message="Failed to fetch trending animes.",
    )


@router.get("/list-anime/vod/{vod_name}")
def list_animes_vod(
    vod_name: str,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_VOD,
        req=req,
        message=f"Failed to fetch animes from VOD service: {vod_name}.",
    )


@router.get("/list-anime/year/{year_series}s")
def list_animes_year_series(
    year_series: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_YEAR_SERIES,
        req=req,
        message=f"Failed to fetch animes from year series: {year_series}s.",
    )


@router.get("/list-anime/year/{year}")
def list_animes_year_specific(
    year: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    req.path_params["year_series"] = floor(year / 10) * 10

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_YEAR_SPECIFIC,
        req=req,
        message=f"Failed to fetch animes from year: {year}.",
    )


@router.get("/list-anime/year/{year}/{season_id}")
def list_animes_year_season(
    year: int,
    season_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_YEAR_SEASON,
        req=req,
        message=f"Failed to fetch animes from year: {year} with season ID: {season_id}.",
    )


@router.get("/list-anime/company/{company_id}")
def list_animes_company(
    company_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_COMPANY,
        req=req,
        message=f"Failed to fetch animes with company ID: {company_id}.",
    )


@router.get("/list-anime/tag/{tag}")
def list_animes_tag(
    tag: str,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_TAG,
        req=req,
        message=f"Failed to fetch animes with tag: {tag}.",
    )


@router.get("/list-anime/person/{person_id}")
def list_animes_person(
    person_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_ANIMES_PERSON,
        req=req,
        message=f"Failed to fetch animes with person ID: {person_id}.",
    )
