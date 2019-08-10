from marshmallow import fields
from marshmallow import Schema


class SmsRequestParameters(Schema):
    national_number = fields.String(required=True, description='National Number')
    country_code = fields.String(
        required=True, description='Country Code, like 86 for China'
    )


class ValidateSmsCodeParameters(Schema):
    code = fields.String(required=True, description='SMS Code')
    phone_num = fields.String(
        required=True, description='Concatted Phone Number, like 8613333333333'
    )
