from aiocron import crontab
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from math import floor
from os import environ
from src.scrape.scrape_service import search_scrape_drama, info_scrape_drama
from src.utility.lib import Logger, MsgSpecJSONResponse
from src.utility.models import Filmarks, SearchParams
from typing import Annotated, Any, Dict


api = FastAPI(
    title="MarkuAPI",
    default_response_class=MsgSpecJSONResponse,
)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/")
def index() -> Dict[str, Any]:

    return {
        "detail": "A basic web scraper API for Filmarks Dramas.",
    }


@api.get("/search/dramas")
def search_dramas(search_params: Annotated[SearchParams, Depends()], req: Request) -> Dict[str, Any]:

    return search_scrape_drama(
        endpoint=Filmarks.Endpoints.SEARCH_DRAMAS.value,
        req=req,
        message="Failed to search dramas.",
    )


@api.get("/dramas/{drama_series_id}/{drama_season_id}")
def info_dramas(drama_series_id: int, drama_season_id: int, req: Request) -> Dict[str, Any]:

    return info_scrape_drama(
        endpoint=Filmarks.Endpoints.INFO_DRAMAS.value,
        req=req,
        message=f"Failed to retrieve drama information with series ID: {drama_series_id} and season ID: {drama_season_id}.",
    )


@api.get("/list-drama/trend")
def list_dramas_trending(search_params: Annotated[SearchParams, Depends()], req: Request) -> Dict[str, Any]:

    return search_scrape_drama(
        endpoint=Filmarks.Endpoints.LIST_DRAMAS_TRENDING.value,
        req=req,
        message="Failed to fetch trending dramas.",
    )


@api.get("/list-drama/country/{country_id}")
def list_dramas_country(country_id: int, search_params: Annotated[SearchParams, Depends()], req: Request) -> Dict[str, Any]:

    return search_scrape_drama(
        endpoint=Filmarks.Endpoints.LIST_DRAMAS_COUNTRY.value,
        req=req,
        message=f"Failed to fetch dramas from country with ID: {country_id}.",
    )


@api.get("/list-drama/year/{year}")
def list_dramas_year(year: int, search_params: Annotated[SearchParams, Depends()], req: Request) -> Dict[str, Any]:
    req.path_params["year_series"] = floor(year / 10) * 10

    return search_scrape_drama(
        endpoint=Filmarks.Endpoints.LIST_DRAMAS_YEAR.value,
        req=req,
        message=f"Failed to fetch dramas from year: {year}.",
    )


@crontab("*/15 * * * *")
async def heartbeat() -> None:

    try:
        async with AsyncClient() as client:
            await client.get(environ.get("BASE"))
            Logger.info("Self-ping succeeded.")

    except Exception:
        Logger.exception("Self-ping failed.")
