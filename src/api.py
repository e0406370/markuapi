from aiocron import crontab
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from src.routers import anime, drama, movie
from src.utility.lib import Logger, MsgSpecJSONResponse
from tomllib import load
from typing import Any, Dict
import os

tags = [
    {
        "name": "anime",
        "description": "Endpoints for retrieving data from **[Filmarks Animes (フィルマークス・アニメ)](https://filmarks.com/animes)**",
    },
    {
        "name": "drama",
        "description": "Endpoints for retrieving data from **[Filmarks Dramas (フィルマークス・ドラマ)](https://filmarks.com/dramas)**",
    },
    {
        "name": "movie",
        "description": "Endpoints for retrieving data from **[Filmarks Movies (フィルマークス・映画)](https://filmarks.com)**",
    },
]


api = FastAPI(
    title="MarkuAPI",
    summary="Web scraper API for Filmarks Animes, Filmarks Dramas, and Filmarks Movies.",
    version=load(open(file="./pyproject.toml", mode="rb"))["project"]["version"],
    contact={"name": "e0406370", "url": "https://github.com/e0406370/markuapiz"},
    openapi_tags=tags,
    redoc_url=None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1, "docExpansion": "none"},
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


@api.get("/", include_in_schema=False)
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
