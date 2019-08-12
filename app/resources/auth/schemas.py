from flask_marshmallow import Schema
from marshmallow import fields

from .models import EnumGender
from app.models.enum_field import EnumField


class CreateAuthClientParameters(Schema):
    class Meta:
        strict = True

    phone_num = fields.String(required=True, description='Phone Number')
    password = fields.String(required=True, description='password')


class PhoneExistParameters(Schema):
    phone_num = fields.String(required=True, description='Phone Number')


class RegisterClientParameters(Schema):
    sex = EnumField(EnumGender, by_value=True, description='gender type', required=True)
    phone_num = fields.String(description='phone_num', required=True)
    password = fields.String(description='password', required=True)
    first_name = fields.String(description='first_name')
    last_name = fields.String(description='last_name', required=True)
    email = fields.Email(description='email', required=True)


class ResetPasswordParameters(Schema):
    phone_num = fields.String(required=True, description='User Id')
    new_password = fields.String(required=True, description='New Password')


class CheckUserIdentificationParameters(Schema):
    id_path = fields.Url(required=True, description='Uploaded Id file path')
