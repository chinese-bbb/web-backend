from app.models import Complaint
from app import db


class ComplaintDAO(object):
    def __init__(self):
        self.OK = "OK"

    # def get(self, id):
    #     for todo in self.todos:
    #         if todo['id'] == id:
    #             return todo
    #     api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):

        complaint = Complaint(user_id=data['user_id'])
        complaint.complaint_body = data['complaint_body']
        complaint.expected_solution_body = data['expected_solution_body']
        complaint.complain_type = data['complain_type']
        complaint.if_comm_by_merchant = data['if_comm_by_merchant']
        complaint.if_public = data['if_public']
        complaint.if_media_report = data['if_media_report']
        complaint.item_price = data['item_price']
        complaint.item_model = data['item_model']
        complaint.purchase_timestamp = data['purchase_timestamp']

        db.session.add(complaint)
        db.session.commit()
        return "OK"

    # def update(self, id, data):
    #     todo = self.get(id)
    #     todo.update(data)
    #     return todo
    #
    # def delete(self, id):
    #     todo = self.get(id)
    #     self.todos.remove(todo)
