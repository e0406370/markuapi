from fastapi import HTTPException, Request
from src.scrape.info_drama_scraper import InfoDramaScraper
from src.scrape.search_drama_scraper import SearchDramaScraper
from src.utility.lib import CustomException, Logger
from typing import Any, Dict


def search_scrape_drama(endpoint: Dict[str, str], req: Request, message: str) -> Dict[str, Any]:
    try:
        scraper = SearchDramaScraper.scrape(endpoint, req)
        scraper.set_search_results()

        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception(message)

        raise CustomException.server_error()


def info_scrape_drama(endpoint: Dict[str, str], req: Request, message: str) -> Dict[str, Any]:
    try:
        scraper = InfoDramaScraper.scrape(endpoint, req)
        scraper.set_info_data()

        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception(message)

        raise CustomException.server_error()