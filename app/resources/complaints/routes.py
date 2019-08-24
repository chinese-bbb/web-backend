import logging

from flask import session
from flask.views import MethodView

from .schemas import changeAuditStatusParameters
from .schemas import ComplaintByMerchantParameters
from .schemas import ComplaintByTypeParameters
from .schemas import ComplaintByUserParameters
from .schemas import ComplaintResponseSchema
from .schemas import ComplaintSchema
from .schemas import LastNComplaintsParameters
from .services import ComplaintDAO
from app.extensions.flask_login_role import login_required
from flask_rest_api import Blueprint

log = logging.getLogger(__name__)

bp = Blueprint(
    'complaints',
    'complaints',
    url_prefix='/complaints',
    description='Complaint Resources API',
)

complaintDAO = ComplaintDAO()


@bp.route('')
class Complaint(MethodView):
    @login_required(role='ANY')
    @bp.arguments(ComplaintSchema)
    def post(self, data):
        """
        Create a Complaint.
        """
        user_id = session['user_id']

        data['user_id'] = user_id
        data['allow_contact_by_merchant'] = True
        data['complaint_status'] = 'initialized'
        data['audit_status'] = 'auditing'

        # TODO: check whether merchant_id exists or not
        res = complaintDAO.create(data)
        if res == 'OK':
            return {'state': 'Success'}
        else:
            return {'state': 'failed creating complaint'}, 422


@bp.route('/byUser')
class ComplaintByUser(MethodView):
    @bp.doc(description='get Complaint by username (phone_num)')
    @bp.arguments(ComplaintByUserParameters, location='query')
    @bp.response(ComplaintResponseSchema(many=True))
    @login_required(role='ANY')
    def get(self, args):
        """
        get Complaint by username  (phone_num)
        """

        phone_num = args['phone_num']
        res = complaintDAO.fetchByUserId(phone_num)
        return res


@bp.route('/byMerchant')
class ComplaintByMerchant(MethodView):
    @bp.doc(description='get Complaint by merchant_id')
    @bp.arguments(ComplaintByMerchantParameters, location='query')
    @bp.response(ComplaintResponseSchema(many=True))
    @login_required(role='ANY')
    def get(self, args):
        """
        get Complaint by merchant_id (merchant_id)
        """

        merchant_id = args['merchant_id']
        res = complaintDAO.fetchByMerchantId(merchant_id)
        return res


@bp.route('/byType')
class ComplaintByType(MethodView):
    @bp.doc(description='get Complaints by complaint type')
    @bp.arguments(ComplaintByTypeParameters, location='query')
    @bp.response(ComplaintResponseSchema(many=True))
    @login_required(role='ANY')
    def get(self, args):
        """
        get Complaint by complain_type.
        """

        complaint_type = args['complaint_type']
        res = complaintDAO.fetchByComplaintType(complaint_type)
        return res


@bp.route('/last')
class ComplaintLatest5(MethodView):
    @bp.doc(description='get latest N complaints')
    @bp.arguments(LastNComplaintsParameters, location='query')
    @bp.response(ComplaintResponseSchema(many=True))
    def get(self, args):
        """
        get latest N complaints order by complaint_time.
        """

        size = args['n']
        res = complaintDAO.getLatestNComplaint(size)
        return res


@bp.route('/all')
class ComplaintAll(MethodView):
    @login_required(role='admin')
    @bp.doc(description='get all complaints')
    @bp.response(ComplaintResponseSchema(many=True))
    def get(self):
        """
        get latest 5 complaints order by complaint_time.
        """

        res = complaintDAO.getAllComplaint()
        return res


@bp.route(
    '/<int:id>',
    parameters=[{'name': 'id', 'in': 'path', 'description': 'complaint id'}],
)
class ComplaintById(MethodView):
    @login_required(role='ANY')
    @bp.response(ComplaintResponseSchema())
    def get(self, id):
        """
        get a complaint by complaint_id.
        """
        res = complaintDAO.get(id)
        return res

    @login_required(role='ANY')
    @bp.doc(description='delete a comment')
    def delete(self, id):
        """
        Delete a complaint by complaint id.
        """
        res = complaintDAO.delete(id)
        if res == 'deleted':
            return '', 204
        else:
            return {'state': 'delete unsuccessful'}


@bp.route('/allAuditing')
class ComplaintAllAuditing(MethodView):
    @login_required(role='admin')
    @bp.response(ComplaintResponseSchema(many=True))
    def get(self):
        """
        get all complaints being audited.
        """

        res = complaintDAO.getAllAuditingComplaint()
        return res


@bp.route('/changeAuditStatus')
class ComplaintChangeStatus(MethodView):
    @bp.arguments(changeAuditStatusParameters)
    @bp.response(ComplaintResponseSchema)
    @login_required(role='admin')
    def put(self, args):
        """
        change Complaint audit_type.
        """
        audit_status = args['audit_status']
        id = args['complaint_id']

        res = complaintDAO.changeComplaintStatus(id, audit_status)
        return res, 200
