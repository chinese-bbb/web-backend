import json
from datetime import datetime

from dateutil import parser
from marshmallow import fields
from marshmallow_sqlalchemy import TableSchema

from app.extensions import api
from app.extensions import db
from app.resources.merchants.models import MerchantQueryRaw
from app.resources.users.models import User
from app.resources.users.schemas import UserSchema


class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merchant_id = db.Column(db.Integer, index=True)
    complaint_body = db.Column(db.String(20000))
    expected_solution_body = db.Column(db.String(20000))
    complain_type = db.Column(db.String(140))
    complaint_status = db.Column(db.String(140))
    complain_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    if_negotiated_by_merchant = db.Column(db.Boolean(), default=False)
    negotiate_timestamp = db.Column(db.DateTime, index=True)
    allow_public = db.Column(db.Boolean(), default=False)
    allow_contact_by_merchant = db.Column(db.Boolean(), default=False)
    allow_press = db.Column(db.Boolean(), default=False)
    item_price = db.Column(db.String(200))
    item_model = db.Column(db.String(200))
    trade_info = db.Column(db.String(20000))
    relatedProducts = db.Column(db.String(5000))
    purchase_timestamp = db.Column(db.DateTime, index=True)

    invoice_files = db.Column(db.String(2000))
    evidence_files = db.Column(db.String(2000))


class ComplaintState(fields.String):
    def _jsonschema_type_mapping(self):
        return {
            'type': 'string',
            'enum': [
                'initialized',
                'Merchant_write_back',
                'in_communication',
                'unresolved',
                'resolved',
            ],
        }


class ComplaintResponse(TableSchema):
    class Meta:
        table = Complaint.__table__
        exclude = ('id', 'complaint_status')
        many = True

    complaint_id = fields.String(attribute='id')
    user = fields.Nested(UserSchema, many=False)
    complaint_state = ComplaintState(attribute='complaint_status')


class ComplaintsResponse(TableSchema):
    ComplaintsResponse = fields.List(fields.Nested(ComplaintResponse), required=True)


complaint_resp_schema = ComplaintResponse()
complaints_resp_schema = ComplaintsResponse(many=True)
user_schema = UserSchema()


def complaint_to_json(complaint):
    user = complaint.User
    dump_user_data = user_schema.dump(user).data
    dump_data = complaint_resp_schema.dump(complaint).data

    # convert string to json array format.
    dump_data['evidence_files'] = json.loads(dump_data['evidence_files'])
    dump_data['invoice_files'] = json.loads(dump_data['invoice_files'])
    dump_data['user'] = dump_user_data
    return dump_data


class ComplaintDAO(object):
    def __init__(self):
        self.OK = 'OK'

    def get(self, complaint_id):
        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if complaint:
            return complaint_to_json(complaint)

        api.abort(404, "Complaint {} doesn't exist".format(complaint_id))

    def delete(self, complaint_id):
        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if complaint:
            db.session.delete(complaint)
            db.session.commit()
            return 'deleted'
        else:
            api.abort(404, "Complaint by id {} doesn't exist".format(complaint))

    def create(self, data):

        if 'negotiate_timestamp' in data and data['negotiate_timestamp'] != '':
            data['negotiate_timestamp'] = parser.parse(data['negotiate_timestamp'])
        else:
            # if the input entry doesn't come with negotiate time, so do a very old time.
            data['negotiate_timestamp'] = None

        data['purchase_timestamp'] = parser.parse(data['purchase_timestamp'])

        if 'invoice_files' in data:
            data['invoice_files'] = json.dumps(data['invoice_files'])
        else:
            data['invoice_files'] = '[]'

        if 'evidence_files' in data:
            data['evidence_files'] = json.dumps(data['evidence_files'])
        else:
            data['evidence_files'] = '[]'

        complaint = Complaint(**data)
        db.session.add(complaint)
        db.session.commit()
        return 'OK'

    def fetchByUserId(self, phone_num):

        user = User.query.filter_by(username=phone_num).first()
        if user is None:
            return {'error': 'User cannot be found'}, 404

        complaints = Complaint.query.filter(Complaint.user_id == user.id).all()
        if complaints:
            ret = []
            for complaint in complaints:
                dump_data = complaint_to_json(complaint)
                ret.append(dump_data)
            return ret
        else:
            return {}

    def fetchByMerchantId(self, merchant_id):

        merchant = MerchantQueryRaw.query.filter_by(id=merchant_id).first()
        if merchant is None:
            return {'error': 'Merchant cannot be found in Merchant Tbale'}, 404

        complaints = Complaint.query.filter_by(merchant_id=merchant_id).all()
        if complaints:
            ret = []
            for complaint in complaints:
                dump_data = complaint_to_json(complaint)
                ret.append(dump_data)
            return ret
        else:
            return {}

    def fetchByComplaintType(self, complain_type):

        complaints = Complaint.query.filter_by(complain_type=complain_type).all()
        if complaints:
            ret = []
            for complaint in complaints:
                dump_data = complaint_to_json(complaint)
                ret.append(dump_data)
            return ret
        else:
            return {}

    def getAllComplaint(self):
        complaints = Complaint.query.all()
        if complaints:
            ret = []
            for complaint in complaints:
                dump_data = complaint_to_json(complaint)
                ret.append(dump_data)
            return ret
        else:
            return {}

    def getLatestNComplaint(self, num):

        complaints = Complaint.query.order_by(
            Complaint.complain_timestamp.desc()
        ).limit(num)
        if complaints:
            ret = []
            for complaint in complaints:
                dump_data = complaint_to_json(complaint)
                ret.append(dump_data)
            return ret
        else:
            return {}
