import flask
from flask import session, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import application, db, api
from app.models import User, FuzzySearchRaw, MerchantQueryRaw
from app.sms.send_sms import send_message
from app.qichacha.qichacha_api import fuzzy_search, basic_detail
from flask_restplus import Resource, fields
import datetime
import json
import werkzeug
import os
from app.complaintDAO import ComplaintDAO
from datetime import datetime
from dateutil import parser
from app.utils import parseBoolean

ns = api.namespace('api', description='All API descriptions')

complaintDAO = ComplaintDAO()


file_upload = ns.parser()
file_upload.add_argument('pic_file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='file')
file_upload.add_argument('sequence',
                         type=str,
                         required=True,
                         help='the sequence order of pictures',
                         location='form')

@ns.route('/upload_invoice')
class InvoiceFileUpload(Resource):
    '''Upload Invoice'''

    @login_required
    @api.doc(parser=file_upload)
    @api.expect(file_upload)
    def post(self):
        print(session)
        user_id = session["user_id"]
        args = file_upload.parse_args()
        print(args['pic_file'].mimetype)
        if args['pic_file'].mimetype == 'image/jpeg':
            destination = os.path.join(application.config.get('WORKING_FOLDER'),
                                       user_id,
                                       application.config.get('INVOICE_FOLDER') + '/')
            if not os.path.exists(destination):
                os.makedirs(destination)
            pic_file = '%s%s' % (destination, args['sequence'] + '.jpeg')
            print(pic_file)
            args['pic_file'].save(pic_file)
            return {"state": "Success", "path": pic_file}, 200
        else:
            return {"state": "failed uploading"}, 401


@ns.route('/upload_id')
class IDUpload(Resource):
    '''Upload ID card'''

    @login_required
    @api.doc(parser=file_upload)
    @api.expect(file_upload)
    def post(self):
        print(session)
        user_id = session["user_id"]
        args = file_upload.parse_args()
        print(args['pic_file'].mimetype)
        if args['pic_file'].mimetype == 'image/jpeg':
            destination = os.path.join(application.config.get('WORKING_FOLDER'),
                                       user_id,
                                       application.config.get('ID_FOLDER') + '/')
            if not os.path.exists(destination):
                os.makedirs(destination)
            pic_file = '%s%s' % (destination, args['sequence'] + '.jpeg')
            print(pic_file)
            args['pic_file'].save(pic_file)
            return {"state": "Success", "path": pic_file}, 200

        else:
            return {"state": "failed uploading"}, 401


complaint_fields = api.model('ComplaintModel', {
    'complaint_body': fields.String(description='complaint body', required=True),
    'expected_solution_body': fields.String(description='expected_solution_body'),
    'complain_type': fields.String(description='complain_type'),
    'if_public': fields.Boolean(description='whether to be public'),
    'if_comm_by_merchant': fields.Boolean(description='whether to communicated by merchant'),
    'if_media_report': fields.Boolean(description='whether to have media report it'),
    'item_price': fields.String(description='item_price'),
    'item_model': fields.String(description='item_model'),
    'purchase_timestamp': fields.DateTime(description='purchase_timestamp')
})


@ns.route('/complaint')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class Complaint(Resource):

    # @ns.doc('get_todo')
    # @ns.marshal_with(todo)
    # def get(self, id):
    #     '''Fetch a given resource'''
    #     return DAO.get(id)
    #
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
        data['purchase_timestamp'] = parser.parse(data['purchase_timestamp'])

        data['if_public'] = parseBoolean(data['if_public'])
        data['if_comm_by_merchant'] = parseBoolean(data['if_comm_by_merchant'])
        data['if_media_report'] = parseBoolean(data['if_media_report'])

        res = complaintDAO.create(data)
        if res == "OK":
            return {"state": "Success"}, 200
        else:
            return {"state": "failed creating complaint"}, 401
