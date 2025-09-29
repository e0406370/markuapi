from fastapi import APIRouter, Depends, Request
from math import floor
from src.scrape.scrape_service import info_scrape, review_scrape, search_scrape
from src.utility.endpoints import Endpoint
from src.utility.models import InfoResponse, ReviewParams, ListParams, SearchParams, SearchResponse
from typing import Annotated

router = APIRouter()


@router.get("/search/dramas", tags=["drama"], response_model=SearchResponse, summary="Search for dramas")
def search_dramas(
    search_params: Annotated[SearchParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.SEARCH_DRAMAS,
        req=req,
        message="Failed to search dramas.",
    )


@router.get("/dramas/{drama_series_id}/{drama_season_id}", tags=["drama"], response_model=InfoResponse, summary="Retrieve information about a specific drama")
def info_dramas(
    drama_series_id: int,
    drama_season_id: int,
    req: Request
) -> InfoResponse:

    return info_scrape(
        endpoint=Endpoint.INFO_DRAMAS,
        req=req,
        message=f"Failed to retrieve information for drama with series ID: {drama_series_id} and season ID: {drama_season_id}.",
    )


@router.get("/dramas/{drama_series_id}/{drama_season_id}/reviews", tags=["drama"], response_model=InfoResponse, summary="Retrieve user reviews about a specific drama")
def review_dramas(
    drama_series_id: int,
    drama_season_id: int,
    review_params: Annotated[ReviewParams, Depends()],
    req: Request
) -> InfoResponse:

    return review_scrape(
        endpoint=Endpoint.REVIEW_DRAMAS,
        req=req,
        message=f"Failed to retrieve reviews for drama with series ID: {drama_series_id} and season ID: {drama_season_id}.",
    )


@router.get("/list-drama/trend", tags=["drama"], response_model=SearchResponse, summary="Fetch currently trending dramas")
def list_dramas_trending(
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_TRENDING,
        req=req,
        message="Failed to fetch trending dramas.",
    )


@router.get("/list-drama/vod/{vod_name}", tags=["drama"], response_model=SearchResponse, summary="Fetch dramas available on a specific VOD service")
def list_dramas_vod(
    vod_name: str,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_VOD,
        req=req,
        message=f"Failed to fetch dramas from VOD service: {vod_name}.",
    )


@router.get("/list-drama/year/{year_series}s", tags=["drama"], response_model=SearchResponse, summary="Fetch dramas released in a specific decade")
def list_dramas_year_series(
    year_series: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_YEAR_SERIES,
        req=req,
        message=f"Failed to fetch dramas from year series: {year_series}s.",
    )


@router.get("/list-drama/year/{year}", tags=["drama"], response_model=SearchResponse, summary="Fetch dramas released in a specific year")
def list_dramas_year_specific(
    year: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    req.path_params["year_series"] = floor(year / 10) * 10

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_YEAR_SPECIFIC,
        req=req,
        message=f"Failed to fetch dramas from year: {year}.",
    )


@router.get("/list-drama/country/{country_id}", tags=["drama"], response_model=SearchResponse, summary="Fetch dramas from a specific country")
def list_dramas_country(
    country_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_COUNTRY,
        req=req,
        message=f"Failed to fetch dramas with country ID: {country_id}.",
    )


@router.get("/list-drama/genre/{genre_id}", tags=["drama"], response_model=SearchResponse, summary="Fetch dramas categorised under a specific genre")
def list_dramas_genre(
    genre_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_GENRE,
        req=req,
        message=f"Failed to fetch dramas with genre ID: {genre_id}.",
    )


@router.get("/list-drama/tag/{tag}", tags=["drama"], response_model=SearchResponse, summary="Fetch dramas categorised under a specific tag")
def list_dramas_tag(
    tag: str,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_TAG,
        req=req,
        message=f"Failed to fetch dramas with tag: {tag}.",
    )


@router.get("/list-drama/person/{person_id}", tags=["drama"], response_model=SearchResponse, summary="Fetch dramas linked to a specific person")
def list_dramas_person(
    person_id: int,
    list_params: Annotated[ListParams, Depends()],
    req: Request
) -> SearchResponse:

    return search_scrape(
        endpoint=Endpoint.LIST_DRAMAS_PERSON,
        req=req,
        message=f"Failed to fetch dramas with person ID: {person_id}.",
    )
