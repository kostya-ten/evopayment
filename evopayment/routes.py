import logging
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

logger = logging.getLogger('evopayment')


class BaseRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            extra = {
                'action': 'api',
                'method': request.method,
                'user-agent': request.headers.get('user-agent', 'n/a'),
                'ip': request.headers.get('x-real-ip', 'n/a'),
            }

            if request.url.path != '/api/v1/health/check/':
                logger.info(msg=f'{request.method} {request.url.path}', extra=extra)

            response: Response = await original_route_handler(request)
            return response

        return custom_route_handler
