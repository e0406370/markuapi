from datetime import datetime, timezone
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from lib import Logger, MsgSpecJSONResponse
from search import search_dramas
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


@api.get("/")
def index() -> Dict[str, Any]:
    return {
        "message": "A basic web scraper API for Filmarks Dramas.",
    }


@api.get("/search/dramas/{query}")
def search(query: str, response: Response) -> Dict[str, Any]:
    try:
        dramas = search_dramas(query)

        response.status_code = status.HTTP_200_OK
        return {
            "query": query,
            "dramas": dramas,
            "scrape_date": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        Logger.exception("Failed to search dramas.")

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "message": "An unexpected error occurred."
        }
