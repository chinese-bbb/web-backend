import logging
import os

log = logging.getLogger(__name__)


class Config(object):
    ENABLED_RESOURCES = (
        'auth',
        'complaints',
        'comments',
        'merchants',
        'users',
        'tools',
    )

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get('SECRET_KEY')
    HOST_IP = os.environ.get('HOST_IP')

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    ) or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db')

    log.info(SQLALCHEMY_DATABASE_URI)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WORKING_FOLDER = os.environ.get('WORKING_FOLDER')

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
