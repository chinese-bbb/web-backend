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

ns = api.namespace('complain', description='Complaint Module')

file_upload = ns.parser()
file_upload.add_argument('pic_file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='file')
file_upload.add_argument('sequence',  type=str, required=True, help='the order of pictures', location='form')

@ns.route('/upload_invoice')
class InvoiceFileUpload(Resource):
    '''Upload Invoice'''

    @login_required
    @api.doc(parser=file_upload)
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
        else:
            {"state": "failed uploading"}, 401
        return {"state": "Success"},200

@ns.route('/upload_id')
class IDUpload(Resource):
    '''Upload Invoice'''

    @login_required
    @api.doc(parser=file_upload)
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
        else:
            {"state": "failed uploading"}, 401
        return {"state": "Success"},200

