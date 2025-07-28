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
    def info(cls, message):
        cls.logger.info(message)

    @classmethod
    def warn(cls, message):
        cls.logger.warning(message)

    @classmethod
    def err(cls, message):
        cls.logger.error(message)


class MsgSpecJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        return msgspec.json.encode(content)
