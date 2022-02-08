from uuid import UUID

from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime
from .. import typeof, store
from ..exceptions import NotFoundException


class Merchant(BaseModel):
    """ Merchant """

    merchant_id: typeof.MerchantID
    token: UUID
    site_id: str
    notification_url: AnyHttpUrl
    created_at: datetime
    updated_at: datetime

    @classmethod
    async def get_by_id(cls, merchant_id: typeof.MerchantID) -> 'Merchant':
        """
        Получить мерчанта по ID

        :param merchant_id: ID мерчанта
        :type merchant_id: typeof.MerchantID
        :return: Merchant
        """
        merchant = await store.merchant.Merchant.get_or_none(merchant_id=merchant_id)
        if merchant is None:
            raise NotFoundException('Merchant is not found')

        return cls.parse_obj(merchant)

    @classmethod
    async def get_by_site_id(cls, site_id: typeof.SiteID) -> 'Merchant':
        """
        Получить мерчанта по SiteID

        :param site_id: SiteID мерчанта
        :type site_id: typeof.SiteID
        :return: Merchant
        """

        merchant = await store.merchant.Merchant.get_or_none(site_id=site_id)
        if merchant is None:
            raise NotFoundException('Merchant is not found')

        return await cls.get_by_id(merchant_id=typeof.MerchantID(merchant.merchant_id))


get_by_id = Merchant.get_by_id
get_by_site_id = Merchant.get_by_site_id
