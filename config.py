import logging
import os

log = logging.getLogger(__name__)


class Config:
    # NOTE: resource order is relevant
    ENABLED_RESOURCES = (
        'auth',
        'complaints',
        'comments',
        'users',
        'merchants',
        'sms',
        'uploads',
    )

    API_VERSION = '1.0'
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/docs'
    OPENAPI_SWAGGER_UI_PATH = '/swagger'
    OPENAPI_SWAGGER_UI_VERSION = '3.23.4'

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    # flask env
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

    # sqlalchemy env
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    ) or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db')

    log.info(SQLALCHEMY_DATABASE_URI)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WORKING_FOLDER = os.environ.get('WORKING_FOLDER')
    INVOICE_FOLDER = 'Invoices'
    EVIDENCE_FOLDER = 'Evidences'
    ID_FOLDER = 'Id'

    if os.environ.get('REMEMBER_COOKIE_DOMAIN'):
        REMEMBER_COOKIE_DOMAIN = os.environ.get('REMEMBER_COOKIE_DOMAIN')

    if os.environ.get('SESSION_COOKIE_DOMAIN'):
        SESSION_COOKIE_DOMAIN = os.environ.get('SESSION_COOKIE_DOMAIN')

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    AWS_S3_PATH_PREFIX = os.environ.get('AWS_S3_PATH_PREFIX')

    TENCENTCLOUD_SECRET_ID = os.environ.get('TENCENTCLOUD_SECRET_ID')
    TENCENTCLOUD_SECRET_KEY = os.environ.get('TENCENTCLOUD_SECRET_KEY')
