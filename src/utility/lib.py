import logging
import msgspec
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Any


class CustomException:
    @staticmethod
    def not_found(detail: str = "The requested resource could not be found.") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    @staticmethod
    def server_error(detail: str = "The server encountered an unexpected error.") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

    @staticmethod
    def service_unavailable(detail: str = "The service is currently unavailable.") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
        )


class Logger:
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    @classmethod
    def info(cls, message: str) -> None:
        cls.logger.info(message)

    @classmethod
    def warn(cls, message: str) -> None:
        cls.logger.warning(message)

    @classmethod
    def err(cls, message: str) -> None:
        cls.logger.error(message)

    @classmethod
    def exception(cls, message: str) -> None:
        cls.logger.exception(message)


class MsgSpecJSONResponse(JSONResponse):
    @classmethod
    def render(cls, content: Any) -> bytes:
        return msgspec.json.encode(content)

    @classmethod
    def parse(cls, content: Any, type: Any) -> Any:
        return msgspec.json.decode(content, type=type)
