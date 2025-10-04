from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache  #noqa: F401
from fastapi_cache.types import Backend
from redis import asyncio as aioredis
from redis.exceptions import ConnectionError
from src.utility.config import Config
from src.utility.lib import Logger
from typing import Optional, Tuple, override


class NoOpBackend(Backend):
    @override
    async def get(self, key: str) -> Optional[bytes]:  # pragma: no cover
        return None

    @override
    async def set(self, key: str, value: bytes, expire: Optional[int] = None) -> None:  # pragma: no cover
        pass

    @override
    async def clear(self, namespace: Optional[str] = None, key: Optional[str] = None) -> int:  # pragma: no cover
        return 0

    @override
    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:  # pragma: no cover
        return 0, None


class SafeRedisBackend(RedisBackend):
    @override
    async def get_with_ttl(self, key: str) -> Tuple[int, Optional[bytes]]:  # pragma: no cover
        async with self.redis.pipeline(transaction=False) as pipe:  # transaction is set to False to prevent this Redis error: "Error in get_with_ttl: unknown command 'EXEC'"
            return await pipe.ttl(key).get(key).execute()


def lifespan_factory(enable_cache: bool, flush_cache: bool):
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        FastAPICache._init = False

        if not enable_cache:
            FastAPICache.init(backend=NoOpBackend())
            Logger.warn("Redis caching disabled - configuration.")

            yield
            return

        try:
            redis = aioredis.from_url(
                url=Config.REDIS_SCHEME,
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                username=Config.REDIS_USERNAME,
                password=Config.REDIS_PASSWORD
            )
            await redis.ping()

            if flush_cache:
                await redis.flushall()
                Logger.warn("Redis cache flushed on startup.")

            FastAPICache.init(backend=SafeRedisBackend(redis), prefix="fastapi-cache")
            Logger.info("Redis caching enabled.")

        except ConnectionError:
            FastAPICache.init(backend=NoOpBackend())
            Logger.exception("Redis caching disabled - connection issue.")

        except Exception:
            FastAPICache.init(backend=NoOpBackend())
            Logger.exception("Redis caching disabled - unexpected error.")

        yield

    return lifespan
