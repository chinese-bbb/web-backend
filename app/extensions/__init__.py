# encoding: utf-8
# pylint: disable=invalid-name,wrong-import-position,wrong-import-order
"""
Extensions setup
================

Extensions provide access to common resources of the application.

Please, put new extension instantiations and initializations here.
"""
from flask import Blueprint
from flask_cors import CORS
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from sqlalchemy_utils import force_auto_coercion
from sqlalchemy_utils import force_instant_defaults

from .flask_sqlalchemy import SQLAlchemy
from .logging import Logging


logging = Logging()

cross_origin_resource_sharing = CORS(supports_credentials=True)

db = SQLAlchemy()

force_auto_coercion()
force_instant_defaults()

login_manager = LoginManager()

marshmallow = Marshmallow()


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(  # pylint: disable=invalid-name
    version='1.0', title='HuXin API', description='Huxin API v1', doc='/doc/'
)


def init_app(app):
    """
    Application extensions initialization
    =====================================
    """
    for extension in (
        logging,
        cross_origin_resource_sharing,
        db,
        login_manager,
        marshmallow,
        api,
    ):
        extension.init_app(app)

    app.register_blueprint(blueprint)
