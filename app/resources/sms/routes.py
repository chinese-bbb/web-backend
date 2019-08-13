import logging
import random

from flask import abort
from flask import after_this_request
from flask import request
from flask.views import MethodView

from .schemas import SmsRequestParameters
from .schemas import ValidateSmsCodeParameters
from app.services.tencent.send_sms import send_message
from flask_rest_api import Blueprint


log = logging.getLogger(__name__)

bp = Blueprint('SMS', 'SMS', url_prefix='/auth/sms', description='SMS Related API')

# Dictionary to store sms verification code
messageDict = {}


@bp.route('/request')
class RequestSmsCode(MethodView):
    @bp.arguments(SmsRequestParameters)
    def post(self, args):
        """
        Get verification code for a phone number.
        """
        rand_num = random.randint(1000, 9999)
        msg = send_message(args['national_number'], args['country_code'], rand_num)
        sid = msg['sid']
        messageDict[sid] = str(rand_num)
        log.debug(rand_num)
        return {'state': 'Success'}, 200, {'Set-Cookie': 'sid=' + sid}


@bp.route('/validate')
class ValidateSmsCode(MethodView):
    @bp.arguments(ValidateSmsCodeParameters)
    def post(self, args):
        """
        Verify the verification number.
        """
        v_code = args['code']

        sid = self._check_cookie_sid()

        if messageDict[sid] != v_code:
            return {'error': 'verification code is not correct'}, 401
        return {'state': 'Success'}

    def _check_cookie_sid(self):
        if request.cookies.get('sid') is None:
            abort(403, "The cookie doesn't come with sid entry")

        @after_this_request
        def set_register_cookie(response):
            response.set_cookie('phone_auth', 'yes', max_age=64800)
            return response

        return request.cookies.get('sid')
