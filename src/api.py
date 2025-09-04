from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import anime, drama, movie
from src.utility.lib import MsgSpecJSONResponse
from typing import Any, Dict


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
api.include_router(anime.router)
api.include_router(drama.router)
api.include_router(movie.router)


@api.get("/")
def index() -> Dict[str, Any]:

    return {
        "detail": "Web scraper API for Filmarks Animes, Filmarks Dramas, and Filmarks Movies.",
    }
