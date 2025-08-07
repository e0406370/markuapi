from fastapi import HTTPException
from src.scrape.info_drama_scraper import InfoDramaScraper
from src.scrape.search_drama_scraper import SearchDramaScraper
from src.utility.lib import CustomException, Logger
from typing import Any, Dict


def search_scrape_drama(endpoint: str, params: Dict, message: str) -> Dict[str, Any]:
    try:
        scraper = SearchDramaScraper.scrape(endpoint, params)
        scraper.set_search_results()

        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception(message)

        raise CustomException.server_error()


def info_scrape_drama(endpoint: str, params: Dict, message: str) -> Dict[str, Any]:
    try:
        scraper = InfoDramaScraper.scrape(endpoint, params)
        scraper.set_info_data()

        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception(message)

        raise CustomException.server_error()