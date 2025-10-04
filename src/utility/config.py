from dataclasses import dataclass
import os


@dataclass
class Config:
    REDIS_ENABLE_CACHE: bool = os.getenv("REDIS_ENABLE_CACHE", "false").lower() == "true"
    REDIS_FLUSH_CACHE: bool = os.getenv("REDIS_FLUSH_CACHE", "false").lower() == "true"
    REDIS_TTL_CACHE: int = int(os.getenv("REDIS_TTL_CACHE", 900))  # 15 minutes

    REDIS_SCHEME: str = os.getenv("REDIS_SCHEME", "redis://")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    REDIS_USERNAME: str = os.getenv("REDIS_USERNAME", "")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")
