from flask import abort

from app.extensions import db
from app.resources.complaints.models import Complaint
from app.resources.merchants.models import MerchantQueryRaw
from app.resources.users.models import User


class ComplaintDAO(object):
    def __init__(self):
        self.OK = 'OK'

    def get(self, complaint_id):
        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if complaint:
            return complaint

        abort(404, "Complaint {} doesn't exist".format(complaint_id))

    def delete(self, complaint_id):
        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if complaint:
            db.session.delete(complaint)
            db.session.commit()
            return 'deleted'
        else:
            abort(404, "Complaint by id {} doesn't exist".format(complaint))

    def create(self, data):
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
            return complaints
        else:
            return []

    def fetchByMerchantId(self, merchant_id):

        merchant = MerchantQueryRaw.query.filter_by(id=merchant_id).first()
        if merchant is None:
            return {'error': 'Merchant cannot be found in Merchant Tbale'}, 404

        complaints = Complaint.query.filter_by(merchant_id=merchant_id).all()
        if complaints:
            return complaints
        else:
            return []

    def fetchByComplaintType(self, complain_type):

        complaints = Complaint.query.filter_by(complain_type=complain_type).all()
        if complaints:
            return complaints
        else:
            return []

    def getAllComplaint(self):
        complaints = Complaint.query.all()
        if complaints:
            return complaints
        else:
            return []

    def getLatestNComplaint(self, num):

        complaints = (
            Complaint.query.order_by(Complaint.complain_timestamp.desc())
            .limit(num)
            .all()
        )
        if complaints:
            return complaints
        else:
            return []

    def getAllAuditingComplaint(self):
        complaints = Complaint.query.filter_by(audit_status="auditing")
        if complaints:
            return complaints
        else:
            return []

    def changeComplaintStatus(self, complaint_id, audit_status):

        complaint = Complaint.query.filter_by(id=complaint_id).first()
        if not complaint:
            abort(404, "Complaint {} doesn't exist".format(complaint_id))

        complaint.audit_status = audit_status
        db.session.commit()
        return complaint
