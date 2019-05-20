from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flasgger import Swagger
from flask_restplus import Resource, Api


application = Flask(__name__)
swagger = Swagger(application)

application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)
login = LoginManager(application)
login.login_view = 'login'

api = Api(application, version='1.0', title='HuXin API',
    description='Huxin API v1', doc='/doc/'
)

from app import routes, models
from app import routes2
