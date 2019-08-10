import logging

from flask import current_app as app
from flask import session
from flask.views import MethodView
from flask_login import login_required
from flask_rest_api import Blueprint

from .schemas import FileUploadFilesParameters
from .schemas import FileUploadFormParameters
from .services import save_temp_file
from app.services.aws.s3 import amazon_s3

log = logging.getLogger(__name__)

bp = Blueprint('uploads', 'uploads', url_prefix='/', description='Shared Upload API')


@bp.route('/upload_file')
class FileUpload(MethodView):
    """
    Upload File.
    """

    @login_required
    @bp.doc(consumes=['multipart/form-data'])
    @bp.arguments(FileUploadFormParameters, location='form')
    @bp.arguments(FileUploadFilesParameters, location='files')
    def post(self, args1, args):
        log.debug(session)
        user_id = session['user_id']

        upload_type = args1['upload_type'].value

        file_path = save_temp_file(upload_type, user_id, args['pic_file'])
        folder = app.config.get(f'{upload_type.upper()}_FOLDER')

        pic_path = amazon_s3.upload_file(file_path, folder)

        return {'state': 'Success', 'path': pic_path}, 200
