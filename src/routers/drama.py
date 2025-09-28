from fastapi import APIRouter, Depends, Request
from math import floor
from src.scrape.scrape_service import info_scrape, review_scrape, search_scrape
from src.utility.endpoints import Endpoint
from src.utility.models import ReviewParams, SearchParams
from typing import Annotated, Any, Dict

router = APIRouter()


@router.get("/search/dramas")
def search_dramas(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.SEARCH_DRAMAS,
        req=req,
        message="Failed to search dramas.",
    )


@router.get("/dramas/{drama_series_id}/{drama_season_id}")
def info_dramas(
    drama_series_id: int,
    drama_season_id: int,
    req: Request
) -> Dict[str, Any]:

    return info_scrape(
        endpoint=Endpoint.INFO_DRAMAS,
        req=req,
        message=f"Failed to retrieve information for drama with series ID: {drama_series_id} and season ID: {drama_season_id}.",
    )


@router.get("/dramas/{drama_series_id}/{drama_season_id}/reviews")
def review_dramas(
    drama_series_id: int,
    drama_season_id: int,
    review_params: Annotated[ReviewParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return review_scrape(
        endpoint=Endpoint.REVIEW_DRAMAS,
        req=req,
        message=f"Failed to retrieve reviews for drama with series ID: {drama_series_id} and season ID: {drama_season_id}.",
    )


@router.get("/list-drama/trend")
def list_dramas_trending(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_TRENDING,
        req=req,
        message="Failed to fetch trending dramas.",
    )


@router.get("/list-drama/vod/{vod_name}")
def list_dramas_vod(
    vod_name: str,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_VOD,
        req=req,
        message=f"Failed to fetch dramas from VOD service: {vod_name}.",
    )


@router.get("/list-drama/year/{year_series}s")
def list_dramas_year_series(
    year_series: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_YEAR_SERIES,
        req=req,
        message=f"Failed to fetch dramas from year series: {year_series}s.",
    )


@router.get("/list-drama/year/{year}")
def list_dramas_year_specific(
    year: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    req.path_params["year_series"] = floor(year / 10) * 10

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_YEAR_SPECIFIC,
        req=req,
        message=f"Failed to fetch dramas from year: {year}.",
    )


@router.get("/list-drama/country/{country_id}")
def list_dramas_country(
    country_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_COUNTRY,
        req=req,
        message=f"Failed to fetch dramas with country ID: {country_id}.",
    )


@router.get("/list-drama/genre/{genre_id}")
def list_dramas_genre(
    genre_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_GENRE,
        req=req,
        message=f"Failed to fetch dramas with genre ID: {genre_id}.",
    )


@router.get("/list-drama/tag/{tag}")
def list_dramas_tag(
    tag: str,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_TAG,
        req=req,
        message=f"Failed to fetch dramas with tag: {tag}.",
    )


@router.get("/list-drama/person/{person_id}")
def list_dramas_person(
    person_id: int,
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> Dict[str, Any]:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_PERSON,
        req=req,
        message=f"Failed to fetch dramas with person ID: {person_id}.",
    )
