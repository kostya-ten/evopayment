import httpx
import pytest

from evopayment.http_base_client import HttpBaseClient


@pytest.mark.asyncio
async def test_http_base_client(app):
    async with HttpBaseClient() as client:
        response: httpx.Response = await client.get(url='https://httpbin.org/get')
        assert response.json().get('headers').get('Accept')
        assert response.json().get('headers').get('Accept-Encoding')
        assert response.json().get('headers').get('Accept-Language')
        assert response.json().get('headers').get('User-Agent')
