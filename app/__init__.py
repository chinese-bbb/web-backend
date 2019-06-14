from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flasgger import Swagger
from flask_restplus import Resource, Api
from flask_cors import CORS

from sqlalchemy import MetaData

application = Flask(__name__)
CORS(application, supports_credentials=True)

swagger = Swagger(application)

application.config.from_object(Config)

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# db = SQLAlchemy(app=application)
db = SQLAlchemy(app=application, metadata=MetaData(naming_convention=naming_convention))

migrate = Migrate(application, db)
with application.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(application, db, render_as_batch=True)
    else:
        migrate.init_app(application, db)

login = LoginManager(application)

api = Api(application, version='1.0', title='HuXin API',
    description='Huxin API v1', doc='/doc/'
)

from app import models
from app import auth_api
from app import complaint_api
from app import merchant_query_api
from app import comment_api
