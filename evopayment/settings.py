import os
import secrets
import string
from enum import Enum

from pydantic import BaseSettings, SecretStr, DirectoryPath, AnyUrl, RedisDsn, Field


class LogLevel(str, Enum):
    debug: str = 'DEBUG'
    info: str = 'INFO'
    warning: str = 'WARNING'
    fatal: str = 'FATAL'


class Settings(BaseSettings):
    """ Configuration class """

    base_dir: DirectoryPath = Field(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    debug: bool = False
    project_host: AnyUrl = Field('https://evopayment.ru')
    log_level: LogLevel = Field('INFO')

    db_host: str = 'localhost'
    db_port: int = 5432
    db_user: str = 'evopayment'
    db_password: SecretStr = Field('password')
    db_database: str = 'evopayment'
    db_schema: str = 'public'
    db_application_name: str = 'evopayment'

    db_min_size: int = 5
    db_max_size: int = 20
    db_max_queries: int = 50000
    max_inactive_connection_lifetime: float = 300.0

    http_client_timeout = 10
    http_client_max_keepalive_connections = 5
    http_client_max_connections = 10

    # Redis
    redis_dsn: RedisDsn = Field('redis://redis:6379')
    redis_password: SecretStr = Field(None)

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


if os.getenv('PYTEST'):  # pragma: no cover
    settings = Settings(
        _env_file=f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/.env',
        _env_file_encoding='utf-8',
    )  # type: ignore

    rnd = ''.join(secrets.choice(string.ascii_letters) for x in range(8))
    settings.db_schema = f'testing_{rnd}'

else:  # pragma: no cover
    settings = Settings()

# ORM Config
ORM_CONFIG = {
    'connections': {
        'master': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'user': settings.db_user,
                'password': settings.db_password.get_secret_value(),
                'host': settings.db_host,
                'port': settings.db_port,
                'database': settings.db_database,
                'min_size': settings.db_min_size,
                'max_size': settings.db_max_size,
                'max_queries': settings.db_max_queries,
                'max_inactive_connection_lifetime': settings.max_inactive_connection_lifetime,
                'application_name': settings.db_application_name,
                'schema': settings.db_schema,
                'ssl': False,
            },
        },
    },
    'apps': {
        'models': {
            'models': [
                # 'aerich.models',
                'evopayment.store.merchant',
            ],
            'default_connection': 'master',
        },
    },
}
