from aiocron import crontab
from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from os import environ
from src.utility.lib import Logger, MsgSpecJSONResponse
from src.utility.models import Filmarks, SearchParams
from src.scrape.scrape_service import search_scrape_drama, info_scrape_drama
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
def search_dramas(search_params: Annotated[SearchParams, Query()], req: Request) -> Dict[str, Any]:

    return search_scrape_drama(
        endpoint=Filmarks.SearchEP.DRAMAS.value,
        params=req.query_params,
        message="Failed to search dramas.",
    )


@api.get("/dramas/{drama_series_id}/{drama_season_id}")
def info_dramas(drama_series_id: int, drama_season_id: int, req: Request) -> Dict[str, Any]:

    return info_scrape_drama(
        endpoint=Filmarks.InfoEP.DRAMAS.value,
        params=req.path_params,
        message="Failed to retrieve drama information.",
    )


@api.get("/list-drama/trend")
def list_dramas_trending(search_params: Annotated[SearchParams, Query()], req: Request) -> Dict[str, Any]:

    return search_scrape_drama(
        endpoint=Filmarks.SearchEP.DRAMAS_TRENDING.value,
        params=req.query_params,
        message="Failed to list trending dramas.",
    )


@crontab("*/15 * * * *")
async def heartbeat() -> None:

    try:
        async with AsyncClient() as client:
            await client.get(environ.get("BASE", "http://127.0.0.1:8000"))
            Logger.info("Self-ping succeeded.")

    except Exception:
        Logger.exception("Self-ping failed.")
