import logging

from flask import session
from flask_login import login_required
from flask_restplus import Namespace
from flask_restplus import Resource
from marshmallow_jsonschema import JSONSchema

from .models import User
from .schemas import UserSchema
from app.extensions import api

log = logging.getLogger(__name__)

ns = Namespace('users', path='/users', description='User Resources API')

user_schema = UserSchema()
json_schema = JSONSchema()

complaint_marshall_model = api.schema_model(
    'UserSchema', json_schema.dump(user_schema).data['definitions']['UserSchema']
)


@ns.route('/me')
class UserMe(Resource):
    """Only Logged in user can see this page."""

    @login_required
    @ns.response(200, 'Success', complaint_marshall_model)
    def get(self):
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()
        dump_data = user_schema.dump(user).data
        return dump_data
