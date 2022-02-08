import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from .. import routes

logger = logging.getLogger('evopayment')
router = APIRouter(tags=['Health check'], prefix='/health/check', route_class=routes.BaseRoute)


@router.get(
    path='/',
    summary='Health check',
    response_model=dict,
    operation_id='health_check',
)
@router.head(
    path='/',
    summary='Health check',
    response_model=dict,
)
async def get():
    """Checking server status"""
    return JSONResponse(status_code=status.HTTP_200_OK, content={})
