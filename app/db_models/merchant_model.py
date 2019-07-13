from marshmallow import fields
from marshmallow_sqlalchemy import TableSchema

from app.models import FuzzySearchRaw
from app.models import MerchantQueryRaw


class MerchantResponse(TableSchema):
    class Meta:
        table = MerchantQueryRaw.__table__
        exclude = ('id', 'keyword')

    merchant_id = fields.String(attribute='id')


merchant_resp = MerchantResponse()


class MerchantSearchResponse(TableSchema):
    class Meta:
        table = FuzzySearchRaw.__table__
        exclude = ('id', 'keyword', 'storage', 'pageIndex')

    result = fields.String()


merchant_search_resp = MerchantSearchResponse()
