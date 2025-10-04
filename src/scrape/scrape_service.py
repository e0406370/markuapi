from fastapi import HTTPException, Request
from src.scrape.info.info_anime_scraper import InfoAnimeScraper
from src.scrape.info.info_drama_scraper import InfoDramaScraper
from src.scrape.info.info_movie_scraper import InfoMovieScraper
from src.scrape.search.search_anime_scraper import SearchAnimeScraper
from src.scrape.search.search_drama_scraper import SearchDramaScraper
from src.scrape.search.search_movie_scraper import SearchMovieScraper
from src.utility.endpoints import Endpoint
from src.utility.lib import CustomException, Logger
from src.utility.utils import ViewType
from typing import Any, Dict


def search_scrape(endpoint: Endpoint, req: Request, message: str) -> Dict[str, Any]:
    try:
        match endpoint.value.view:
            case ViewType.ANIME:
                scraper = SearchAnimeScraper.scrape(endpoint, req)

            case ViewType.DRAMA:
                scraper = SearchDramaScraper.scrape(endpoint, req)

            case ViewType.MOVIE:
                scraper = SearchMovieScraper.scrape(endpoint, req)

            case _:  # pragma: no cover
                raise ValueError(f"Unexpected ViewType: {endpoint.value.view}")

        scraper.set_search_results()
        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception(message)
        raise CustomException.server_error()


def info_scrape(endpoint: Endpoint, req: Request, message: str) -> Dict[str, Any]:
    try:
        match endpoint.value.view:
            case ViewType.ANIME:
                scraper = InfoAnimeScraper.scrape(endpoint, req)

            case ViewType.DRAMA:
                scraper = InfoDramaScraper.scrape(endpoint, req)

            case ViewType.MOVIE:
                scraper = InfoMovieScraper.scrape(endpoint, req)

            case _:  # pragma: no cover
                raise ValueError(f"Unexpected ViewType: {endpoint.value.view}")

        scraper.set_info_data()
        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception(message)
        raise CustomException.server_error()


def review_scrape(endpoint: Endpoint, req: Request, message: str) -> Dict[str, Any]:
    try:
        match endpoint.value.view:
            case ViewType.ANIME:
                scraper = InfoAnimeScraper.scrape(endpoint, req)

            case ViewType.DRAMA:
                scraper = InfoDramaScraper.scrape(endpoint, req)

            case ViewType.MOVIE:
                scraper = InfoMovieScraper.scrape(endpoint, req)

            case _:  # pragma: no cover
                raise ValueError(f"Unexpected ViewType: {endpoint.value.view}")

        scraper.set_review_data()
        return scraper.get_response()

    except HTTPException:
        raise

    except Exception:
        Logger.exception(message)
        raise CustomException.server_error()
