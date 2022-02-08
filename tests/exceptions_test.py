import pytest

from evopayment.exceptions import (
    RMQConnectionErrorException,
    BadRequestException,
    NotFoundIPAddressException,
)


@pytest.mark.asyncio
async def test_exception_rmq_connection_error(app):
    with pytest.raises(RMQConnectionErrorException):
        raise RMQConnectionErrorException()


@pytest.mark.asyncio
async def test_exception_bad_request(app):
    with pytest.raises(BadRequestException):
        raise BadRequestException()


@pytest.mark.asyncio
async def test_exception_not_found_ip_address(app):
    with pytest.raises(NotFoundIPAddressException):
        raise NotFoundIPAddressException()
