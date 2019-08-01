import enum
import logging

from flask import session
from flask_login import login_required
from flask_restplus import fields
from flask_restplus import Namespace
from flask_restplus import Resource
from marshmallow_jsonschema import JSONSchema

from .models import complaint_resp_schema
from .models import ComplaintDAO
from .models import complaints_resp_schema
from app.extensions import api
from app.utils import parseBoolean


log = logging.getLogger(__name__)

json_schema = JSONSchema()

complaints_marshall_model = api.schema_model(
    'ComplaintsResponse',
    json_schema.dump(complaints_resp_schema).data['definitions']['ComplaintsResponse'][
        'properties'
    ]['ComplaintsResponse'],
)


ns = Namespace('complaints', path='/complaints', description='Complaint Resources API')

complaintDAO = ComplaintDAO()


class EnumComplaintType(enum.Enum):
    product_issue = 'product_issue'
    fake_add = 'fake_ad'
    customer_service = 'customer_service'
    exchange_return = 'exchange_return'
    warranty = 'warranty'
    contract = 'contract'
    shipping = 'shipping'
    infraction = 'infraction'
    other = 'others'


file_fields = api.model('file', {'s3_path': fields.String})

complaint_fields = api.model(
    'ComplaintModel',
    {
        'merchant_id': fields.Integer(description='merchant ID', required=True),
        'complaint_body': fields.String(description='complaint body', required=True),
        'expected_solution_body': fields.String(description='expected_solution_body'),
        'complain_type': fields.String(
            description='The complaint type', enum=EnumComplaintType._member_names_
        ),
        'if_negotiated_by_merchant': fields.Boolean(description='if_negotiated'),
        'negotiate_timestamp': fields.DateTime(description='negotiate_timestamp'),
        'allow_public': fields.Boolean(description='whether to be public'),
        'allow_contact_by_merchant': fields.Boolean(
            description='whether to communicated by merchant'
        ),
        'allow_press': fields.Boolean(description='whether to have media report it'),
        'item_price': fields.String(description='item_price'),
        'item_model': fields.String(description='item_model'),
        'trade_info': fields.String(description='tradeInfo'),
        'relatedProducts': fields.String(description='relatedProducts'),
        'purchase_timestamp': fields.DateTime(description='purchase_timestamp'),
        'invoice_files': fields.List(fields.Nested(file_fields)),
        'evidence_files': fields.List(fields.Nested(file_fields)),
    },
)

complaint_list = api.model(
    'ComplaintListModel',
    {'complaint_list': fields.List(fields.Nested(complaint_fields))},
)

complaint_parser = api.parser()
complaint_parser.add_argument(
    'complaint_id', type=int, required=True, help='complaint id', location='args'
)


@ns.route('/')
@ns.route('')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class Complaint(Resource):
    @login_required
    @api.expect(complaint_fields)
    def post(self):
        """Create a Complaint."""
        data = api.payload
        user_id = session['user_id']

        data['user_id'] = user_id
        data['if_negotiated_by_merchant'] = parseBoolean(
            data['if_negotiated_by_merchant']
        )
        data['allow_public'] = parseBoolean(data['allow_public'])

        # TODO: if allow_contact_by_merchant key doesn't exist, what we do.

        if 'invoice_files' not in data:
            data['allow_contact_by_merchant'] = True

        # data['allow_contact_by_merchant'] = parseBoolean(data['allow_contact_by_merchant'])
        data['allow_contact_by_merchant'] = True
        data['allow_press'] = parseBoolean(data['allow_press'])
        data['complaint_status'] = 'initialized'

        # TODO: check whether merchant_id exists or not
        res = complaintDAO.create(data)
        if res == 'OK':
            return {'state': 'Success'}, 200
        else:
            return {'state': 'failed creating complaint'}, 401


complaintByUser_parser = api.parser()
complaintByUser_parser.add_argument(
    'phone_num', type=str, required=True, help='complaint id', location='args'
)


@ns.route('/byUser')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class ComplaintByUser(Resource):
    @ns.doc('get Complaint by username (phone_num)')
    @api.doc(parser=complaintByUser_parser)
    @api.expect(complaintByUser_parser)
    @ns.response(200, 'Success', complaints_marshall_model)
    @login_required
    def get(self):
        """get Complaint by username  (phone_num)"""

        args = complaintByUser_parser.parse_args()
        phone_num = args['phone_num']
        res = complaintDAO.fetchByUserId(phone_num)
        return res, 200


complaintByMerchant_parser = api.parser()
complaintByMerchant_parser.add_argument(
    'merchant_id', type=str, required=True, help='complaint id', location='args'
)


@ns.route('/byMerchant')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class ComplaintByMerchant(Resource):
    @ns.doc('get Complaint by merchant_id')
    @api.doc(parser=complaintByMerchant_parser)
    @api.expect(complaintByMerchant_parser)
    @ns.response(200, 'Success', complaints_marshall_model)
    @login_required
    def get(self):
        """get Complaint by merchant_id (merchant_id)"""

        args = complaintByMerchant_parser.parse_args()
        merchant_id = args['merchant_id']
        res = complaintDAO.fetchByMerchantId(merchant_id)
        return res, 200


complaintByType_parser = api.parser()
complaintByType_parser.add_argument(
    'complain_type', type=str, required=True, help='complaint type', location='args'
)


@ns.route('/byType')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class ComplaintByType(Resource):
    @ns.doc('get Complaints by complain_type')
    @api.doc(parser=complaintByType_parser)
    @api.expect(complaintByType_parser)
    @ns.response(200, 'Success', complaints_marshall_model)
    @login_required
    def get(self):
        """get Complaint by complain_type."""

        args = complaintByType_parser.parse_args()
        complain_type = args['complain_type']
        res = complaintDAO.fetchByComplaintType(complain_type)
        return res, 200


complaint_marshall_model = api.schema_model(
    'ComplaintResponse',
    json_schema.dump(complaint_resp_schema).data['definitions']['ComplaintResponse'],
)

complaintLastN_parser = api.parser()
complaintLastN_parser.add_argument(
    'N', type=int, required=True, help='latest complaints', location='args'
)

@ns.route('/last')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class ComplaintLatest5(Resource):
    @ns.doc('get latest N complaints')
    @api.doc(parser=complaintLastN_parser)
    @api.expect(complaintLastN_parser)
    @ns.response(200, 'Success', complaints_marshall_model)
    def get(self):
        """get latest N complaints order by complaint_time"""

        args = complaintLastN_parser.parse_args()
        N = args['N']
        res = complaintDAO.getLatestNComplaint(N)
        return res, 200

@ns.route('/all')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class ComplaintLatest5(Resource):
    @ns.doc('get all complaints')
    @ns.response(200, 'Success', complaints_marshall_model)
    def get(self):
        """get latest 5 complaints order by complaint_time"""

        res = complaintDAO.getAllComplaint()
        return res, 200


@ns.route('/<int:id>')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
@ns.param('id', 'The Complaint Identifier')
class ComplaintById(Resource):
    @login_required
    @ns.response(200, 'Success', complaint_marshall_model)
    def get(self, id):
        """get a Comment by comment_id."""
        res = complaintDAO.get(id)
        return res

    @ns.doc('delete a comment')
    @ns.response(204, 'Comment deleted')
    def delete(self, id):
        """Delete a comment by comment id."""
        res = complaintDAO.delete(id)
        if res == 'deleted':
            return '', 204
        else:
            return {'state': 'delete unsuccessful'}, 200
