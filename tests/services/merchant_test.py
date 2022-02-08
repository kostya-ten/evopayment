import pytest


@pytest.mark.asyncio
async def test_merchant_get(app, merchant):
    assert isinstance(merchant.merchant_id, int)
    assert merchant.site_id == 'fcdv21-00'
    assert merchant.notification_url
