from enum import Enum

from marshmallow import fields

from app.extensions import api

ma_plugin = api.ma_plugin


@ma_plugin.map_to_openapi_type('string', 'binary')
class FileField(fields.Raw):
    pass


class EnumUploadFileType(Enum):
    invoice = 'invoice'
    id = 'id'
    evidence = 'evidence'
