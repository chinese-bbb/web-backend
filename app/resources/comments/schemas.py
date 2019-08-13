from flask_marshmallow.sqla import TableSchema
from marshmallow import fields
from marshmallow import Schema

from .models import Comment
from app.resources.users.schemas import UserSchema


class CreateCommentParameters(Schema):
    text = fields.String(required=True, description='comment text body')
    complaint_id = fields.Int(required=True, description='complaint_id')


class CommentResponseSchema(TableSchema):
    class Meta:
        table = Comment.__table__
        exclude = ['id']

    complaint_id = fields.String(attribute='complaint_id')
    user = fields.Nested(UserSchema, attribute='User')
