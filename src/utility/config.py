from dataclasses import dataclass, field
import os


@dataclass
class Config:
    REDIS_ENABLE_CACHE: bool = os.getenv("REDIS_ENABLE_CACHE", "false").lower() == "true"
    REDIS_FLUSH_CACHE: bool = os.getenv("REDIS_FLUSH_CACHE", "false").lower() == "true"
    REDIS_TTL_CACHE: int = int(os.getenv("REDIS_TTL_CACHE", 1800))  # 30 minutes

    REDIS_SCHEME: str = os.getenv("REDIS_SCHEME", "redis://")
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT", "6379")
    REDIS_USERNAME: str = os.getenv("REDIS_USERNAME", "")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

    LOGGER_LEVEL: str = os.getenv("LOGGER_LEVEL", "INFO").upper()
    
    BLOCKED: frozenset = frozenset(
        ip.strip()
        for ip in os.getenv("BLOCKED_IPS", "").split(",")
        if ip.strip()
    )
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "5/minute")
    LOGTAIL_TOKEN: str = os.getenv("LOGTAIL_TOKEN", "")
