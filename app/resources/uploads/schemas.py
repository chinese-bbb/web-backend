from flask_marshmallow import Schema
from marshmallow import ValidationError

from .models import EnumUploadFileType
from .models import FileField
from app.models.enum_field import EnumField


def file_validate(file):
    if file.mimetype not in ['image/jpeg', 'image/png']:
        raise ValidationError('File format not allowed')


class FileUploadFormParameters(Schema):

    upload_type = EnumField(
        EnumUploadFileType,
        by_value=True,
        required=True,
        description='upload type(invoice/id/evidence)',
        location='form',
    )
    pic_file = FileField(
        required=True,
        validate=file_validate,
        description='image file',
        location='files',
    )
