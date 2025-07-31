import logging
import msgspec
from fastapi.responses import JSONResponse
from typing import Any


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
    def parse(cls, content: Any) -> Any:
        return msgspec.json.decode(content)
