import time
import os

from flask import session
from flask_login import login_user, logout_user, current_user, login_required
from app import application, db, api
from flask_restplus import Resource, fields
import werkzeug
from app.complaintDAO import ComplaintDAO
from app.utils import parseBoolean
from app.aws.s3 import amazon_s3

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


file_fields = api.model('file', {
    'id': fields.Integer,
    's3_path': fields.String
})

complaint_fields = api.model('ComplaintModel', {
    'merchant_id': fields.Integer(description='merchant ID', required=True),
    'complaint_body': fields.String(description='complaint body', required=True),
    'expected_solution_body': fields.String(description='expected_solution_body'),
    'complain_type': fields.String(description='complain_type'),
    'if_negotiated_by_merchant': fields.Boolean(description='if_negotiated'),
    'negotiate_timestamp': fields.DateTime(description='negotiate_timestamp'),
    'allow_public': fields.Boolean(description='whether to be public'),
    'allow_contact_by_merchant': fields.Boolean(description='whether to communicated by merchant'),
    'allow_press': fields.Boolean(description='whether to have media report it'),
    'item_price': fields.String(description='item_price'),
    'item_model': fields.String(description='item_model'),
    'tradeInfo': fields.String(description='tradeInfo'),
    'relatedProducts': fields.String(description='relatedProducts'),
    'purchase_timestamp': fields.DateTime(description='purchase_timestamp'),
    'invoice_files': fields.List(fields.Nested(file_fields)),
    'id_files': fields.List(fields.Nested(file_fields))
})

complaint_list = api.model('ComplaintListModel', {
    'complaint_list': fields.List(fields.Nested(complaint_fields))
})

complaint_parser = api.parser()
complaint_parser.add_argument('complaint_id', type=str, required=True, help='complaint id', location='json')

@ns.route('/complaint')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class Complaint(Resource):

    @ns.doc('get Complaint by complaint_id')
    @api.doc(parser=complaint_parser)
    @api.expect(complaint_parser)
    def get(self):
        '''get Complaint by complaint_id'''

        args = complaint_parser.parse_args()
        complaint_id = args['complaint_id']
        res = complaintDAO.get(complaint_id)
        return res


    # @ns.doc('delete_todo')
    # @ns.response(204, 'Todo deleted')
    # def delete(self, id):
    #     '''Delete a task given its identifier'''
    #     DAO.delete(id)
    #     return '', 204

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

        print(data)

        # TODO: check whether merchant_id exists or not

        res = complaintDAO.create(data)
        if res == "OK":
            return {"state": "Success"}, 200
        else:
            return {"state": "failed creating complaint"}, 401


complaintByUser_parser = api.parser()
complaintByUser_parser.add_argument('phone_num', type=str, required=True, help='complaint id', location='json')

@ns.route('/complaintByUser')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class ComplaintByUser(Resource):

    @ns.doc('get Complaint by username (phone_num)')
    @api.doc(parser=complaintByUser_parser)
    @api.expect(complaintByUser_parser)
    @login_required
    def get(self):
        '''get Complaint by username  (phone_num)'''

        args = complaintByUser_parser.parse_args()
        phone_num = args['phone_num']
        res = complaintDAO.fetchByUserId(phone_num)
        return res


complaintByMerchant_parser = api.parser()
complaintByMerchant_parser.add_argument('merchant_id', type=str, required=True, help='complaint id', location='json')

@ns.route('/complaintByMerchant')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class ComplaintByMerchant(Resource):

    @ns.doc('get Complaint by merchant_id')
    @api.doc(parser=complaintByMerchant_parser)
    @api.expect(complaintByMerchant_parser)
    @login_required
    def get(self):
        '''get Complaint by merchant_id (merchant_id)'''

        args = complaintByMerchant_parser.parse_args()
        merchant_id = args['merchant_id']
        res = complaintDAO.fetchByMerchantId(merchant_id)
        return res