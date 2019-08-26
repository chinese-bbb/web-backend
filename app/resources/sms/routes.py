import logging
import random

import redis
from flask import abort
from flask import after_this_request
from flask import make_response
from flask import request
from flask.views import MethodView

from .schemas import SmsRequestParameters
from .schemas import ValidateSmsCodeParameters
from app.services.tencent.send_sms import send_message
from config import Config
from flask_rest_api import Blueprint

log = logging.getLogger(__name__)

bp = Blueprint('SMS', 'SMS', url_prefix='/auth/sms', description='SMS Related API')

# Dictionary to store sms verification code
messageDict = {}
redis_client = redis.Redis(host=Config.REDIS_ADDR, port=6379)


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

        # Expiring in 300 seconds
        redis_client.set(sid, str(rand_num), ex=300)
        log.debug('phone_num: %s, code: %d', args['national_number'], rand_num)

        resp = make_response({'state': 'Success'})
        resp.set_cookie(
            'sid', sid, secure=True, httponly=True, samesite='LAX', max_age=1800
        )

        return resp


@bp.route('/validate')
class ValidateSmsCode(MethodView):
    @bp.arguments(ValidateSmsCodeParameters)
    def post(self, args):
        """
        Verify the verification number.
        """
        v_code = args['code']

        sid = self._check_cookie_sid()

        value_from_redis = redis_client.get(sid).decode('utf-8')
        print('redis: ' + value_from_redis)
        if value_from_redis != v_code:
            return {'error': 'verification code is not correct'}, 422

        resp = make_response({'state': 'Success'})
        resp.delete_cookie('sid')
        return resp

    def _check_cookie_sid(self):
        if request.cookies.get('sid') is None:
            abort(403, "The cookie doesn't come with sid entry")

        @after_this_request
        def set_register_cookie(response):
            response.set_cookie('phone_auth', 'yes', max_age=1800)
            return response

        return request.cookies.get('sid')
