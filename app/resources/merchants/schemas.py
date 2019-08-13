from marshmallow import fields
from marshmallow import Schema
from marshmallow_sqlalchemy import TableSchema

from app.resources.merchants.models import FuzzySearchRaw


class BasicMerchantSchema(Schema):
    CreditCode = fields.String()
    KeyNo = fields.String(required=True)
    Name = fields.String(required=True)
    No = fields.String(required=True)
    OperName = fields.String()
    StartDate = fields.String()
    Status = fields.String()


class MerchantSchema(BasicMerchantSchema):
    Address = fields.String()
    BelongOrg = fields.String()
    CheckDate = fields.String()
    EconKind = fields.String()
    EndDate = fields.String()
    ImageUrl = fields.URL()
    IsOnStock = fields.String()
    OrgNo = fields.String()
    OriginalName = fields.List(fields.String())
    Province = fields.String()
    RegistCapi = fields.String()
    Scope = fields.String()
    StartDate = fields.String()
    Status = fields.String()
    StockNumber = fields.String()
    StockType = fields.String()
    TeamEnd = fields.String()
    TermStart = fields.String()
    UpdatedDate = fields.String()
    merchant_id = fields.String()


class FuzzyQueryParameters(Schema):
    keyword = fields.String(required=True, description='keyword')


class MerchantSearchParameters(Schema):
    keyword = fields.String(required=True, description='keyword')
    pageIndex = fields.Int(
        required=True, validate=lambda v: 0 <= v < 10000, description='pageIndex'
    )


class MerchantResponseSchema(Schema):
    merchant_id = fields.String()
    storage = fields.Nested(MerchantSchema)


class MerchantSearchResponseSchema(TableSchema):
    class Meta:
        table = FuzzySearchRaw.__table__
        exclude = ('id', 'keyword', 'storage', 'pageIndex')

    result = fields.Nested(BasicMerchantSchema, many=True)
    totalPage = fields.Int()
