import pytest

from evopayment.redis import RedisClient


@pytest.mark.asyncio
async def test_redis(app):
    async with RedisClient() as client:
        assert await client.set('test-key', 'test-value', 10)
        assert await client.get('test-key') == 'test-value'
        assert await client.delete('test-key')


@pytest.mark.asyncio
async def test_redis_exceptions(app):
    with pytest.raises(Exception):
        async with RedisClient():
            raise Exception('test')
