from aiocron import crontab
from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from os import environ
from src.scrape.search_drama_scraper import SearchDramaScraper
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
def search(search_params: Annotated[SearchParams, Query()], req: Request) -> Dict[str, Any]:
    try:
        scraper = SearchDramaScraper.scrape(
            endpoint=Filmarks.SearchEP.DRAMAS.value,
            params=req.query_params
        )

        scraper.set_search_results()

        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception("Failed to search dramas.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The server encountered an unexpected error.",
        )


@crontab("*/15 * * * *")
async def heartbeat() -> None:
    try:
        async with AsyncClient() as client:
            await client.get(environ.get("BASE", "http://127.0.0.1:8000"))
            Logger.info("Self-ping succeeded.")

    except Exception:
        Logger.exception("Self-ping failed.")
