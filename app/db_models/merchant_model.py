from datetime import datetime
from app import application, db, api
from marshmallow_sqlalchemy import ModelSchema, fields_for_model, TableSchema
from app.models import User, MerchantQueryRaw
from app import db, api
from dateutil import parser
import json
from marshmallow import Schema, fields
from marshmallow_sqlalchemy import ModelSchema, fields_for_model, TableSchema
from app.models import UserSchema, MerchantQueryRaw,FuzzySearchRaw


class MerchantResponse(TableSchema):
    class Meta:
        table = MerchantQueryRaw.__table__
        exclude = ("id","keyword")

    merchant_id = fields.String(attribute="id")


merchant_resp = MerchantResponse()

class MerchantSearchResponse(TableSchema):
    class Meta:
        table = FuzzySearchRaw.__table__
        exclude = ("id","keyword","storage","pageIndex")

    result = fields.String()


merchant_search_resp = MerchantSearchResponse()