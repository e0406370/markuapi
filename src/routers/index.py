from typing import Dict
from fastapi import APIRouter

router = APIRouter()


@router.get("/", include_in_schema=False)
def index() -> Dict[str, str]:

    return {
        "detail": "Web scraper API for Filmarks Animes, Filmarks Dramas, and Filmarks Movies.",
    }
