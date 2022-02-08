import logging

import aioredis
from aioredis import Redis
from aioredis.exceptions import ConnectionError as RedisConnectionError

from .exceptions import RedisConnectionErrorException
from .settings import settings

logger = logging.getLogger('iperon')


class RedisClient:
    _inited = False
    redis: Redis

    @classmethod
    async def init(cls):
        if settings.redis_password.get_secret_value():  # pragma: no cover
            cls.redis = aioredis.Redis(
                connection_pool=aioredis.ConnectionPool.from_url(
                    url=settings.redis_dsn,
                    encoding='utf-8',
                    decode_responses=True,
                    max_connections=10,
                    password=settings.redis_password.get_secret_value(),
                )
            )
        else:
            cls.redis = aioredis.Redis(
                connection_pool=aioredis.ConnectionPool.from_url(
                    url=settings.redis_dsn,
                    encoding='utf-8',
                    decode_responses=True,
                    max_connections=10,
                )
            )

        cls._inited = True

    async def __aenter__(self) -> Redis:
        await RedisClient.init()

        try:
            await self.redis.ping()
        except RedisConnectionError as err:  # pragma: no cover
            logger.critical(f'Redis connection error "{err}"')
            raise RedisConnectionErrorException()

        return self.redis

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
