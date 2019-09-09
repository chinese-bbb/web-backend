# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position,wrong-import-order
"""
Extensions setup
================

Extensions provide access to common resources of the application.

Please, put new extension instantiations and initializations here.
"""
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_user import UserManager
from sqlalchemy_utils import force_auto_coercion
from sqlalchemy_utils import force_instant_defaults

from .flask_sqlalchemy import SQLAlchemy
from .logging import Logging
from flask_rest_api import Api
from flask_rest_api import Blueprint

logging = Logging()

cross_origin_resource_sharing = CORS(supports_credentials=True, resources=r'/api/*')

db = SQLAlchemy()

force_auto_coercion()
force_instant_defaults()

marshmallow = Marshmallow()

api_blueprint = Blueprint('api', __name__)
api = Api(title='HuXin API')


def init_app(app):
    """
    Application extensions initialization
    =====================================
    """
    for extension in (api, logging, cross_origin_resource_sharing, db, marshmallow):
        extension.init_app(app)

    from .migrate import init_app as migrate_init
    from app.resources.users.models import User

    UserManager(app, db, User)

    migrate_init(app, db)
