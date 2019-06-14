import time
import os

from flask import session
from flask_login import login_user, logout_user, current_user, login_required
from app import application, db, api
from flask_restplus import Resource, fields
import werkzeug
from app.db_models.complaint_model import ComplaintDAO, complaint_resp_schema, complaints_resp_schema
from app.utils import parseBoolean
from app.aws.s3 import amazon_s3
from marshmallow_jsonschema import JSONSchema

json_schema = JSONSchema()

complaint_marshall_model = api.schema_model('ComplaintResponse',
                                          json_schema.dump(complaint_resp_schema).data['definitions']['ComplaintResponse'])

complaints_marshall_model = api.schema_model('ComplaintsResponse',
            json_schema.dump(complaints_resp_schema)
                       .data['definitions']['ComplaintsResponse']['properties']['ComplaintsResponse'])


ns = api.namespace('api', description='All API descriptions')

complaintDAO = ComplaintDAO()


file_upload = ns.parser()
file_upload.add_argument('upload_type',
                         type=str,
                         required=True,
                         help='upload type(invoice/id/evidence)',
                         location='form')
file_upload.add_argument('pic_file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='file')

@ns.route('/upload_file')
class FileUpload(Resource):
    '''Upload File'''

    @login_required
    @api.doc(parser=file_upload)
    @api.expect(file_upload)
    def post(self):
        print(session)
        user_id = session["user_id"]
        args = file_upload.parse_args()
        if args['upload_type'] not in ['invoice', 'id', 'evidence']:
            return {"state": "incorrect upload type"}, 401
        print(args['pic_file'].mimetype)
        if args['pic_file'].mimetype == 'image/jpeg':
            folder = application.config.get(f"{args['upload_type'].upper()}_FOLDER")
            destination = os.path.join(application.config.get('WORKING_FOLDER'),
                                       user_id,
                                       folder + '/')
            if not os.path.exists(destination):
                os.makedirs(destination)
            pic_file = '%s%s' % (destination, str(int(time.time())) + '.jpeg')
            print(pic_file)
            args['pic_file'].save(pic_file)
            pic_path = amazon_s3.upload_file(pic_file, folder)
            return {"state": "Success", "path": pic_path}, 200
        else:
            return {"state": "failed uploading"}, 401

import enum
class EnumComplaintType(enum.Enum):
    fake_add         = 'fake_ad'
    customer_service = 'customer_service'
    exchange_return  = 'exchange_return'
    warranty         = 'warranty'
    contract         = 'contract'
    shipping         = 'shipping'
    commercial       = 'commercial'
    other = 'others'


file_fields = api.model('file', {
    'id': fields.Integer,
    's3_path': fields.String
})

complaint_fields = api.model('ComplaintModel', {
    'merchant_id': fields.Integer(description='merchant ID', required=True),
    'complaint_body': fields.String(description='complaint body', required=True),
    'expected_solution_body': fields.String(description='expected_solution_body'),
    'complain_type': fields.String(description='The complaint type', enum=EnumComplaintType._member_names_),
    'if_negotiated_by_merchant': fields.Boolean(description='if_negotiated'),
    'negotiate_timestamp': fields.DateTime(description='negotiate_timestamp'),
    'allow_public': fields.Boolean(description='whether to be public'),
    'allow_contact_by_merchant': fields.Boolean(description='whether to communicated by merchant'),
    'allow_press': fields.Boolean(description='whether to have media report it'),
    'item_price': fields.String(description='item_price'),
    'item_model': fields.String(description='item_model'),
    'trade_info': fields.String(description='tradeInfo'),
    'relatedProducts': fields.String(description='relatedProducts'),
    'purchase_timestamp': fields.DateTime(description='purchase_timestamp'),
    'invoice_files': fields.List(fields.Nested(file_fields)),
    'id_files': fields.List(fields.Nested(file_fields))
})

complaint_list = api.model('ComplaintListModel', {
    'complaint_list': fields.List(fields.Nested(complaint_fields))
})

complaint_parser = api.parser()
complaint_parser.add_argument('complaint_id', type=int, required=True, help='complaint id', location='args')

@ns.route('/complaint')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class Complaint(Resource):

    @login_required
    @api.expect(complaint_fields)
    def post(self):
        '''Create a Complaint'''
        data = api.payload
        user_id = session["user_id"]

        data['user_id'] = user_id
        data['if_negotiated_by_merchant'] = parseBoolean(data['if_negotiated_by_merchant'])
        data['allow_public'] = parseBoolean(data['allow_public'])
        data['allow_contact_by_merchant'] = parseBoolean(data['allow_contact_by_merchant'])
        data['allow_press'] = parseBoolean(data['allow_press'])
        data['complaint_status'] = 'initialized'

        # TODO: check whether merchant_id exists or not
        res = complaintDAO.create(data)
        if res == "OK":
            return {"state": "Success"}, 200
        else:
            return {"state": "failed creating complaint"}, 401

@ns.route('/complaint/<int:id>')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
@ns.param('id', 'The Complaint Identifier')
class Comment(Resource):

    @login_required
    @ns.response(200, 'Success', complaint_marshall_model)
    def get(self, id):
        '''get a Comment by comment_id'''
        res = complaintDAO.get(id)
        return res

    @ns.doc('delete a comment')
    @ns.response(204, 'Comment deleted')
    def delete(self, id):
        '''Delete a comment by comment id'''
        res = complaintDAO.delete(id)
        if res == "deleted":
            return '', 204
        else:
            return {"state": "delete unsuccessful"}, 200


complaintByUser_parser = api.parser()
complaintByUser_parser.add_argument('phone_num', type=str, required=True, help='complaint id', location='args')

@ns.route('/complaintByUser')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class ComplaintByUser(Resource):

    @ns.doc('get Complaint by username (phone_num)')
    @api.doc(parser=complaintByUser_parser)
    @api.expect(complaintByUser_parser)
    @ns.response(200, 'Success', complaints_marshall_model)
    @login_required
    def get(self):
        '''get Complaint by username  (phone_num)'''

        args = complaintByUser_parser.parse_args()
        phone_num = args['phone_num']
        res = complaintDAO.fetchByUserId(phone_num)
        return res


complaintByMerchant_parser = api.parser()
complaintByMerchant_parser.add_argument('merchant_id', type=str, required=True, help='complaint id', location='args')

@ns.route('/complaintByMerchant')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class ComplaintByMerchant(Resource):

    @ns.doc('get Complaint by merchant_id')
    @api.doc(parser=complaintByMerchant_parser)
    @api.expect(complaintByMerchant_parser)
    @ns.response(200, 'Success', complaints_marshall_model)
    @login_required
    def get(self):
        '''get Complaint by merchant_id (merchant_id)'''

        args = complaintByMerchant_parser.parse_args()
        merchant_id = args['merchant_id']
        res = complaintDAO.fetchByMerchantId(merchant_id)
        return res