from flask_marshmallow import Schema
from flask_marshmallow.sqla import TableSchema
from marshmallow import fields

from .models import User
from app.models.enum_field import EnumField
from app.resources.auth.models import EnumGender


class UserSchema(TableSchema):
    """
    using TableSchema is to exclude relationship data.
    """

    class Meta:
        table = User.__table__
        exclude = ('id', 'password_hash', 'real_name')
        dump_only = (User.id.key,)

    sex = EnumField(EnumGender, by_value=True, required=True, attribute='sex')


class ChangePasswordParameters(Schema):
    phone_num = fields.String(required=True, description='User Id')
    old_password = fields.String(required=True, description='Old Password')
    new_password = fields.String(required=True, description='New Password')
