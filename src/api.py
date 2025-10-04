from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import anime, drama, index, movie
from src.utility.config import Config
from src.utility.lib import MsgSpecJSONResponse
from src.utility.rediss import lifespan_factory
from tomllib import load


def init_api(enable_cache: bool, flush_cache: bool) -> FastAPI:
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
        contact={"name": "e0406370", "url": "https://github.com/e0406370/markuapi"},
        version=load(open(file="./pyproject.toml", mode="rb"))["project"]["version"],
        openapi_tags=tags,
        redoc_url=None,
        swagger_ui_parameters={"defaultModelsExpandDepth": -1, "docExpansion": "none"},
        default_response_class=MsgSpecJSONResponse,
        lifespan=lifespan_factory(enable_cache, flush_cache),
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
    api.include_router(index.router)
    api.include_router(movie.router)

    return api


api = init_api(
    enable_cache=Config.REDIS_ENABLE_CACHE,
    flush_cache=Config.REDIS_FLUSH_CACHE
)
