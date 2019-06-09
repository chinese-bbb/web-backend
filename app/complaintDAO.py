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
        complaint = Complaint(user_id=data['user_id'])
        complaint.complaint_body = data['complaint_body']
        complaint.expected_solution_body = data['expected_solution_body']
        complaint.complain_type = data['complain_type']
        complaint.merchant_id = data['merchant_id']
        complaint.if_negotiated_by_merchant = data['if_negotiated_by_merchant']

        if 'negotiate_timestamp' in data:
            complaint.negotiate_timestamp = parser.parse(data['negotiate_timestamp'])

        complaint.allow_public = data['allow_public']
        complaint.allow_contact_by_merchant = data['allow_contact_by_merchant']
        complaint.allow_press = data['allow_press']

        complaint.item_price = data['item_price']
        complaint.item_model = data['item_model']
        complaint.relatedProducts = data['relatedProducts']
        complaint.purchase_timestamp = parser.parse(data['purchase_timestamp'])

        if 'invoice_files' in data:
            complaint.invoce_files = json.dumps(data['invoice_files'])

        if 'id_files' in data:
            complaint.invoce_files = json.dumps(data['id_files'])

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
