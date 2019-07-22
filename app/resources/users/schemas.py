from marshmallow_sqlalchemy import TableSchema

from app.resources.users.models import User


class UserSchema(TableSchema):
    class Meta:
        table = User.__table__
        include_fk = True
        exclude = ('id', 'posts', 'password_hash', 'real_name')
        many = True
