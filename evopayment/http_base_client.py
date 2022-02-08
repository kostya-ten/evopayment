import logging

import httpx
from fastapi.applications import FastAPI

from . import __version__
from .settings import settings

logger = logging.getLogger('evopayment')


class HttpBaseClient:
    def __init__(self, base_url: str = '', verify: bool = True, app: FastAPI = None):
        """ Custom http client """

        headers = {
            'User-Agent': f'evopayment/{__version__}',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'application/json',
        }

        self.client = httpx.AsyncClient(
            limits=httpx.Limits(
                max_keepalive_connections=settings.http_client_max_keepalive_connections,
                max_connections=settings.http_client_max_connections,
            ),
            base_url=base_url,
            http2=True,
            verify=verify,
            event_hooks={
                'request': [self.log_request],
                'response': [self.log_response],
            },
            headers=headers,
            timeout=settings.http_client_timeout,
            app=app,
        )

    async def __aenter__(self) -> httpx.AsyncClient:
        return self.client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    @staticmethod
    async def log_request(request: httpx.Request):
        logger.info(f'Request http client: {request.method} {request.url} - Waiting for response')

    @staticmethod
    async def log_response(response: httpx.Response):
        request = response.request
        logger.info(f'Response http client: {request.method} {request.url} - Status {response.status_code}')
