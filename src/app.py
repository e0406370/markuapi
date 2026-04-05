from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from src.routers import anime, drama, index, movie
from src.utility.config import Config
from src.utility.lib import MsgSpecJSONResponse
from src.utility.rediss import lifespan_factory
from tomllib import load

limiter = Limiter(key_func=get_remote_address, default_limits=[Config.RATE_LIMIT])
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
    api.state.limiter = limiter
    api.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    api.add_middleware(SlowAPIMiddleware)
    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @api.middleware("http")
    async def block(request: Request, call_next):
        client_ip = request.client.host
        if client_ip in Config.BLOCKED:
            return JSONResponse(status_code=403, content={"detail": "Forbidden"})
        return await call_next(request)

    api.include_router(anime.router)
    api.include_router(drama.router)
    api.include_router(index.router)
    api.include_router(movie.router)

    return api


app = init_api(
    enable_cache=Config.REDIS_ENABLE_CACHE,
    flush_cache=Config.REDIS_FLUSH_CACHE
)
