from aiocron import crontab
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from src.routers import anime, drama, movie
from src.utility.lib import Logger, MsgSpecJSONResponse
from tomllib import load
from typing import Any, Dict
import os


api = FastAPI(
    title="MarkuAPI",
    version=load(open(file="./pyproject.toml", mode="rb"))["project"]["version"],
    default_response_class=MsgSpecJSONResponse,
)
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
api.include_router(anime.router)
api.include_router(drama.router)
api.include_router(movie.router)


@api.get("/")
def index() -> Dict[str, Any]:

    return {
        "detail": "Web scraper API for Filmarks Animes, Filmarks Dramas, and Filmarks Movies.",
    }


@crontab("*/10 * * * *")
async def heartbeat():

    try:
        async with AsyncClient() as client:
            await client.get(os.environ.get("BASE"))
            Logger.info("Self-ping succeeded.")

    except Exception:
        Logger.exception("Self-ping failed.")
