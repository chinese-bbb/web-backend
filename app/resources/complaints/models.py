from datetime import datetime
from enum import Enum

from sqlalchemy_utils import JSONType

from app.extensions import db


class EnumComplaintType(Enum):
    product_issue = 'product_issue'
    fake_ad = 'fake_ad'
    customer_service = 'customer_service'
    exchange_return = 'exchange_return'
    warranty = 'warranty'
    contract = 'contract'
    shipping = 'shipping'
    infraction = 'infraction'
    other = 'other'


class EnumComplaintState(Enum):
    initialized = 'initialized'
    merchant_commented = 'merchant_commented'
    customer_commented = 'customer_commented'
    unresolved = 'unresolved'
    resolved = 'resolved'


class EnumAuditState(Enum):
    auditing = 'auditing'
    approved = 'approved'
    rejected = 'rejected'


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_body = db.Column(db.Text())
    expected_solution_body = db.Column(db.Text())
    complain_type = db.Column(db.Enum(EnumComplaintType))
    complain_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    if_negotiated_by_merchant = db.Column(db.Boolean(), default=False)
    negotiate_timestamp = db.Column(db.DateTime)
    allow_public = db.Column(db.Boolean(), default=False)
    allow_contact_by_merchant = db.Column(db.Boolean(), default=False)
    allow_press = db.Column(db.Boolean(), default=False)
    item_price = db.Column(db.String(200))
    item_model = db.Column(db.String(200))
    trade_info = db.Column(db.String(1000))
    relatedProducts = db.Column(db.String(1000))
    purchase_timestamp = db.Column(db.DateTime)
    invoice_files = db.Column(JSONType)
    evidence_files = db.Column(JSONType)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant_query_raw.id'))
    complaint_status = db.Column(db.Enum(EnumComplaintState))
    audit_status = db.Column(db.Enum(EnumAuditState))
