import logging, msgspec
from fastapi.responses import JSONResponse
from typing import Any


class Logger:
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    logging.basicConfig(handlers=[handler], level=logging.INFO)
    logger = logging.getLogger(__name__)

    @classmethod
    def info(cls, message: str):
        cls.logger.info(message)

    @classmethod
    def warn(cls, message: str):
        cls.logger.warning(message)

    @classmethod
    def err(cls, message: str):
        cls.logger.error(message)

    @classmethod
    def exception(cls, message: str):
        cls.logger.exception(message)


class MsgSpecJSONResponse(JSONResponse):
    @classmethod
    def render(cls, content: Any) -> bytes:
        return msgspec.json.encode(content)

    @classmethod
    def parse(cls, content: Any) -> Any:
        return msgspec.json.decode(content)
