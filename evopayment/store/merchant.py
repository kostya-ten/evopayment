from tortoise import models, fields


class MerchantModel(models.Model):
    merchant_id: int = fields.IntField(pk=True, title='Merchant ID', description='Merchant ID')

    token = fields.UUIDField()
    site_id = fields.CharField(max_length=10)
    notification_url = fields.CharField(max_length=200)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(now_add=True, auto_now_add=True)

    class Meta:
        table = 'merchant'


Merchant = MerchantModel
