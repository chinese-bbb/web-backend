from flask_marshmallow.sqla import TableSchema
from marshmallow import fields
from marshmallow import pre_load
from marshmallow import Schema

from .models import Complaint
from .models import EnumComplaintState
from .models import EnumComplaintType
from .models import EnumAuditState
from app.models.enum_field import EnumField
from app.resources.users.schemas import UserSchema


class ComplaintSchema(Schema):
    merchant_id = fields.Integer(description='merchant ID', required=True)
    complaint_body = fields.String(description='complaint body', required=True)
    expected_solution_body = fields.String(
        description='expected_solution_body', required=True
    )
    complain_type = EnumField(
        EnumComplaintType,
        by_value=True,
        required=True,
        description='The complaint type',
    )
    if_negotiated_by_merchant = fields.Boolean(
        description='if_negotiated', required=True
    )
    negotiate_timestamp = fields.DateTime(
        description='negotiate_timestamp', allow_none=True
    )
    allow_public = fields.Boolean(description='whether to be public', required=True)
    allow_contact_by_merchant = fields.Boolean(
        description='whether to communicated by merchant'
    )
    allow_press = fields.Boolean(
        description='whether to have media report it', required=True
    )
    item_price = fields.String(description='item_price')
    item_model = fields.String(description='item_model')
    trade_info = fields.String(description='tradeInfo')
    relatedProducts = fields.String(description='relatedProducts')
    purchase_timestamp = fields.DateTime(
        description='purchase_timestamp', required=True
    )
    invoice_files = fields.List(fields.URL(), description='uploaded invoice file list')
    evidence_files = fields.List(
        fields.URL(), description='uploaded evidence file list'
    )

    @pre_load
    def load_data(self, data, **kwargs):
        data['negotiate_timestamp'] = data.get('negotiate_timestamp') or None
        return data


class ComplaintResponseSchema(TableSchema):
    class Meta:
        table = Complaint.__table__
        exclude = ('id', 'complaint_status')

    complaint_id = fields.String(attribute='id', required=True)
    invoice_files = fields.List(
        fields.URL(),
        description='uploaded invoice file list',
        attribute='invoice_files',
    )
    evidence_files = fields.List(
        fields.URL(),
        description='uploaded evidence file list',
        attribute='evidence_files',
    )
    complain_type = EnumField(
        EnumComplaintType, by_value=True, required=True, attribute='complain_type'
    )
    complaint_state = EnumField(
        EnumComplaintState, by_value=True, required=True, attribute='complaint_status'
    )
    audit_status = EnumField(
        EnumAuditState, by_value=True, required=True, attribute='audit_status'
    )
    user = fields.Nested(UserSchema, attribute='User')


class ComplaintByUserParameters(Schema):
    phone_num = fields.String(required=True, description='user id')


class ComplaintByMerchantParameters(Schema):
    merchant_id = fields.String(required=True, description='merchant id')


class ComplaintByTypeParameters(Schema):
    complaint_type = fields.String(required=True, description='complaint type')


class LastNComplaintsParameters(Schema):
    n = fields.Int(required=True, description='latest `n` pieces of complaints')

class changeAuditStatusParameters(Schema):
    audit_status = fields.String(required=True, description='audit status to be replaced.')
    complaint_id = fields.Int(required=True, description='complaint_id')
