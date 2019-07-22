import logging
import os
import time

import werkzeug.datastructures
from flask import current_app as app
from flask import session
from flask_login import login_required
from flask_restplus import Namespace
from flask_restplus import Resource

from app.extensions import api
from app.services.aws.s3 import amazon_s3

log = logging.getLogger(__name__)

ns = Namespace('tools', path='/', description='Shared Tools API')

file_upload = ns.parser()

file_upload.add_argument(
    'upload_type',
    type=str,
    required=True,
    help='upload type(invoice/id/evidence)',
    location='form',
)
file_upload.add_argument(
    'pic_file',
    type=werkzeug.datastructures.FileStorage,
    location='files',
    required=True,
    help='file',
)


@ns.route('/upload_file')
class FileUpload(Resource):
    """Upload File."""

    @login_required
    @api.doc(parser=file_upload)
    @api.expect(file_upload)
    def post(self):
        log.debug(session)
        user_id = session['user_id']
        args = file_upload.parse_args()
        if args['upload_type'] not in ['invoice', 'id', 'evidence']:
            return {'state': 'incorrect upload type'}, 401
        log.debug(args['pic_file'].mimetype)
        if args['pic_file'].mimetype and len(args['pic_file'].mimetype.split('/')) == 2:
            file_type, file_format = args['pic_file'].mimetype.split('/')
            if file_type.lower() != 'image' or file_format.lower() not in [
                'jpeg',
                'jpg',
                'png',
            ]:
                return {'state': 'incorrect file type/format'}, 401
            folder = app.config.get(f"{args['upload_type'].upper()}_FOLDER")
            destination = os.path.join(
                app.config.get('WORKING_FOLDER'), user_id, folder + '/'
            )
            if not os.path.exists(destination):
                os.makedirs(destination)
            pic_file = '%s%s' % (destination, str(int(time.time())) + '.' + file_format)
            log.debug(pic_file)
            args['pic_file'].save(pic_file)
            pic_path = amazon_s3.upload_file(pic_file, folder)
            return {'state': 'Success', 'path': pic_path}, 200
        else:
            return {'state': 'failed uploading'}, 401
