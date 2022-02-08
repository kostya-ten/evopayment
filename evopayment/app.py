import asyncio
import logging
import os

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from tortoise import Tortoise

from . import __version__, logger, handlers, redis
from .exceptions import exception_handlers
from .settings import settings, ORM_CONFIG


app = FastAPI(
    title='Evopayment',
    version=__version__,
    default_response_class=ORJSONResponse,
    docs_url='/api/',
    redoc_url=None,
    openapi_url='/api/v1/openapi.json',
    debug=settings.debug,
    exception_handlers=exception_handlers,  # type: ignore
)

if not settings.debug:  # pragma: no cover
    app.redoc_url = None

# Initialization logger
logger.logger_init()


# Initialization Tortoise
# Waiting for a connection to the DB
async def db_init() -> None:
    log = logging.getLogger('evopayment')

    while True:
        try:
            await Tortoise.init(config=ORM_CONFIG)
        except ConnectionRefusedError as err:  # pragma: no cover
            log.critical(f'PostgresSQL connection error "{err}"')
            await asyncio.sleep(10)
            continue
        else:  # pragma: no cover
            break

    # Create schema
    if connection := Tortoise.get_connection('master'):
        await connection.execute_query(f'CREATE SCHEMA IF NOT EXISTS {settings.db_schema}')

    await Tortoise.generate_schemas()


async def db_shutdown() -> None:
    await Tortoise.close_connections()


@app.on_event('startup')
async def startup_event() -> None:
    log = logging.getLogger('evopayment')

    await db_init()

    # Initialization redis
    await redis.RedisClient.init()

    log.info(f'Startup service pid:{os.getpid()}')


@app.on_event('shutdown')
async def shutdown_event() -> None:
    await db_shutdown()
    await redis.RedisClient.redis.close()


# Registration of routers
app.include_router(handlers.healthcheck.router, prefix='/api/v1')
