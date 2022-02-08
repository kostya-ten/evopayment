import httpx
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(app):

    client = AsyncClient(app=app, base_url='http://localhost.local')
    response: httpx.Response = await client.get(url='/api/v1/health/check/')
    assert response.status_code == 200

    await client.aclose()
