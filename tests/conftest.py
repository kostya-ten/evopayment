import asyncio

import pytest
from tortoise import Tortoise

from evopayment.app import app as evopayment_app
from evopayment.app import startup_event, shutdown_event
from evopayment.settings import settings
from evopayment import store, services, typeof


@pytest.fixture()
async def merchant(event_loop):
    merchant = await store.merchant.MerchantModel.create(
        token='c6052e59-8abe-4cd2-aaa3-7636f027e85d',
        site_id='fcdv21-00',
        notification_url='https://httpbin.org/post',
    )
    srv_merchant = await services.merchant.get_by_id(merchant_id=typeof.MerchantID(merchant.merchant_id))
    yield srv_merchant
    await merchant.delete()


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture()
async def app(event_loop):
    await evopayment_app.on_event('startup')(startup_event())

    await Tortoise.generate_schemas()

    try:
        yield evopayment_app
    finally:
        try:
            connection = Tortoise.get_connection('master')
        except KeyError:
            pass
        else:
            await connection.execute_query(f'DROP SCHEMA IF EXISTS {settings.db_schema} CASCADE')
            await evopayment_app.on_event('shutdown')(shutdown_event())
