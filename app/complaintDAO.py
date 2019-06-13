from app.models import Complaint, ComplaintSchema, User, MerchantQueryRaw
from app import db, api
from dateutil import parser
import json


complaint_schema = ComplaintSchema()
complaints_schema = ComplaintSchema(many=True)

class ComplaintDAO(object):
    def __init__(self):
        self.OK = "OK"

    def get(self, complaint_id):
        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if complaint:
            return complaint_schema.jsonify(complaint)

        api.abort(404, "Complaint {} doesn't exist".format(complaint_id))

    def create(self, data):

        if 'negotiate_timestamp' in data:
            data['negotiate_timestamp'] = parser.parse(data['negotiate_timestamp'])
        else:
            data['negotiate_timestamp'] = "unknown"

        data['purchase_timestamp'] = parser.parse(data['purchase_timestamp'])

        if 'invoice_files' in data:
            data['invoice_files'] = json.dumps(data['invoice_files'])
        else:
            data['invoice_files'] = "unknown"

        if 'id_files' in data:
            data['id_files'] = json.dumps(data['id_files'])
        else:
            data['id_files'] = "unknown"

        complaint = Complaint(**data)
        db.session.add(complaint)
        db.session.commit()
        return "OK"

    def fetchByUserId(self, phone_num):

        user = User.query.filter_by(username=phone_num).first()
        if user is None:
            return {
                       "error": "User cannot be found"
                   }, 404

        complaints = Complaint.query.filter_by(user_id=user.id)
        if complaints:
            return complaints_schema.jsonify(complaints)
        else:
            api.abort(404, "Complaint by user {} doesn't exist".format(phone_num))

    def fetchByMerchantId(self, merchant_id):

        merchant = MerchantQueryRaw.query.filter_by(id=merchant_id).first()
        if merchant is None:
            return {
                       "error": "Merchant cannot be found by this merchant_id"
                   }, 404

        complaints = Complaint.query.filter_by(merchant_id=merchant_id)
        if complaints:
            return complaints_schema.jsonify(complaints)
        else:
            api.abort(404, "Complaint by Merchant id{} doesn't exist".format(merchant_id))



    # def update(self, id, data):
    #     todo = self.get(id)
    #     todo.update(data)
    #     return todo
    #
    # def delete(self, id):
    #     todo = self.get(id)
    #     self.todos.remove(todo)
