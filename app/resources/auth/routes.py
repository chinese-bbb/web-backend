import datetime
import enum
import logging
import random

import flask
import phonenumbers
from flask import after_this_request
from flask import flash
from flask import request
from flask import session
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_restplus import fields
from flask_restplus import Namespace
from flask_restplus import reqparse
from flask_restplus import Resource

from app.extensions import db
from app.resources.users.models import User
from app.services.tencent.id_ocr import tencent_ocr

log = logging.getLogger(__name__)

ns = Namespace('auth', path='/auth', description='Authentication Related API')

# Dictionary to store sms verification code
messageDict = {}


@ns.route('/phone_exist/<string:phone_num>')
@ns.doc(params={'phone_num': 'A phone number'})
class PhoneExist(Resource):
    """Check if phone number is registered."""

    @ns.doc(responses={200: 'Success', 404: 'Validation Error'})
    def get(self, phone_num):
        user = User.query.filter_by(username=phone_num).first()
        log.debug(user)
        if user is None:
            try:
                result = phonenumbers.parse(phone_num, 'CN')
                if result.country_code == 86:
                    phone_num = result.national_number
                user = User.query.filter_by(username=phone_num).first()
            except Exception:
                return {'error': 'Invalid phone num or password'}, 404

            if user is None:
                return {phone_num: 'Not Registerred phone num'}, 404
        return {'state': 'Success'}, 200


reuqest_sms_parser = reqparse.RequestParser()
reuqest_sms_parser.add_argument(
    'national_number', type=str, required=True, help='national_number', location='json'
)
reuqest_sms_parser.add_argument(
    'country_code', type=str, required=True, help='country_code', location='json'
)


@ns.route('/sms/request')
@ns.doc(params={'national_number': 'A phone number', 'country_code': 'country_code'})
@ns.doc(
    responses={200: 'Success', 400: 'Validation Error', 401: 'Passcode is not correct'}
)
class RequestSMS(Resource):
    @ns.doc(parser=reuqest_sms_parser)
    def post(self):
        """Get verification code for a phone number."""
        rand_num = random.randint(1000, 9999)
        reuqest_sms_parser.parse_args()
        # msg = send_message(args['national_number'], args['country_code'], rand_num)
        sid = "msg['sid']"
        messageDict[sid] = str(rand_num)
        log.debug(rand_num)
        return {'state': 'Success'}, 200, {'Set-Cookie': 'sid=' + sid}


validate_sms_parser = reqparse.RequestParser()
validate_sms_parser.add_argument(
    'v_code', type=str, required=True, help='verification code', location='json'
)


@ns.route('/sms/validate')
@ns.doc(params={'v_code': 'sms code'})
@ns.doc(
    responses={200: 'Success', 400: 'Validation Error', 401: 'Passcode is not correct'}
)
class ValidateSMS(Resource):
    @ns.doc(parser=validate_sms_parser)
    def post(self):
        """Verify the verification number."""
        args = validate_sms_parser.parse_args()
        v_code = args['v_code']

        sid = self._check_cookie_sid()

        if messageDict[sid] != v_code:
            return {'error': 'verification code is not correct'}, 401
        return {'state': 'Success'}, 200

    def _check_cookie_sid(self):
        if request.cookies.get('sid') is None:
            ns.abort(403, "The cookie doesn't come with sid entry")

        @after_this_request
        def set_register_cookie(response):
            response.set_cookie('phone_auth', 'yes', max_age=64800)
            return response

        return request.cookies.get('sid')


login_parser = ns.parser()
login_parser.add_argument(
    'phone_num', type=str, required=True, help='Phone Number', location='json'
)
login_parser.add_argument(
    'password', type=str, required=True, help='password', location='json'
)


@ns.route('/login')
@ns.doc(
    responses={
        200: 'Success',
        401: 'Invalid password',
        404: 'User Cannot be found',
        400: 'Validation Error',
    }
)
class Login(Resource):
    @ns.doc(parser=login_parser)
    def post(self):
        """Log in."""
        args = login_parser.parse_args()
        username = args['phone_num']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        log.debug(user)
        if user is None:
            try:
                result = phonenumbers.parse(username, 'CN')
                if result.country_code == 86:
                    username = result.national_number
                user = User.query.filter_by(username=username).first()
            except Exception:
                return {'error': 'Invalid phone num or password'}, 404

            if user is None:
                return {'error': 'Invalid phone num or password'}, 404

        if not user.check_password(password):
            log.debug('Invalid username or password')
            return {'error': 'Invalid phone num or password'}, 401

        login_user(user, remember=True)
        return flask.jsonify('OK')


@ns.route('/logout')
@ns.doc(responses={200: 'Success'})
class Logout(Resource):
    @login_required
    def post(self):
        """Log out."""
        logout_user()
        return {'state': 'Success'}, 200


class EnumSexType(enum.Enum):
    Male = 'Male'
    Female = 'Female'
    other = 'others'


register_fields = ns.model(
    'RegisterModel',
    {
        'sex': fields.String(
            description='gender type', enum=EnumSexType._member_names_, required=True
        ),
        'phone_num': fields.String(description='phone_num', required=True),
        'password': fields.String(description='password', required=True),
        'first_name': fields.String(description='first_name', required=True),
        'last_name': fields.String(description='last_name', required=True),
        'email': fields.String(description='email', required=False),
    },
)


@ns.route('/register')
@ns.doc(responses={200: 'Register Success', 400: 'Validation Error'})
class Register(Resource):
    def _check_cookie_phone_allow(self):
        if request.cookies.get('phone_auth') is None:
            ns.abort(403, "The cookie doesn't come with phone_allow entry")

    @ns.expect(register_fields)
    def post(self):
        """Register a user."""

        self._check_cookie_phone_allow()
        data = ns.payload
        username = data['phone_num']
        sex = data['sex']
        password = data['password']
        if 'email' in data:
            data['email']
        else:
            pass

        today = datetime.date.today()
        user = User(username=username, sex=sex, registered_date=today)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.account_active = True
        user.if_verified = False
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        login_user(user, remember=True)
        return flask.jsonify('OK')


changepwd_parser = ns.parser()
changepwd_parser.add_argument(
    'phone_num', type=str, required=True, help='Phone Number', location='json'
)
changepwd_parser.add_argument(
    'old_password', type=str, required=True, help='password', location='json'
)
changepwd_parser.add_argument(
    'new_password', type=str, required=True, help='password', location='json'
)


@ns.route('/changepw')
@ns.doc(responses={200: 'Success', 400: 'Validation Error'})
class ChangePassword(Resource):
    @ns.doc(parser=changepwd_parser)
    def post(self):
        """Change Password."""

        args = changepwd_parser.parse_args()
        username = args['phone_num']
        old_password = args['old_password']
        new_password = args['new_password']

        user = User.query.filter_by(username=username).first()
        log.debug(user)
        if user is None or not user.check_password(old_password):
            log.debug('Invalid username or password')
            return flask.jsonify({'error': 'Invalid phone num or password'})

        user.set_password(new_password)
        db.session.commit()
        flash('Congratulations, successfully updated user password!')
        return flask.jsonify('OK')


resetpwd_parser = ns.parser()
resetpwd_parser.add_argument(
    'phone_num', type=str, required=True, help='Phone Number', location='json'
)
resetpwd_parser.add_argument(
    'new_password', type=str, required=True, help='new_password', location='json'
)


@ns.route('/resetpw')
@ns.doc(responses={200: 'Success', 400: 'Validation Error'})
class ResetPassword(Resource):
    @ns.doc(parser=resetpwd_parser)
    def post(self):
        """Reset Password."""

        args = resetpwd_parser.parse_args()
        username = args['phone_num']
        new_password = args['new_password']

        user = User.query.filter_by(username=username).first()
        if user is None:
            log.debug('Invalid username')
            return flask.jsonify({'error': 'Invalid phone num'})

        log.debug(user)
        user.set_password(new_password)
        db.session.commit()
        flash('Congratulations, successfully updated user password!')
        return flask.jsonify('OK')


identify_parser = ns.parser()
identify_parser.add_argument(
    'id_path', type=str, required=True, help='upload path', location='json'
)


@ns.route('/identify')
@ns.doc(responses={200: 'Success', 400: 'Validation Error'})
class IdentifyIDCard(Resource):
    @login_required
    @ns.doc(parser=identify_parser)
    def post(self):
        """Identify user ID card."""
        user_id = session['user_id']
        args = identify_parser.parse_args()
        id_path = args['id_path']
        if not id_path:
            return flask.jsonify({'error': 'Invalid image url'})

        # TODO: remove this hack in near future.
        user = User.query.filter_by(id=user_id).first()
        user.if_verified = True
        db.session.commit()
        flash('Congratulations, successfully verified your ID card!')
        return flask.jsonify('OK')

        # TODO: one hack to unblock production.
        real_name, sex = tencent_ocr.identify(id_path)
        if real_name and sex:
            user = User.query.filter_by(id=user_id).first()
            last_name = user.last_name or ''
            first_name = user.first_name or ''
            if (
                (last_name and first_name and last_name + first_name == real_name)
                or (real_name.startswith(last_name))
            ) and user.sex == sex:
                user.real_name = real_name
                user.sex = sex
                user.if_verified = True
                db.session.commit()
                flash('Congratulations, successfully verified your ID card!')
                return flask.jsonify('OK')
            else:
                return flask.jsonify(
                    {'error': "ID card name/sex doesn't match your register name/sex!"}
                )
        return flask.jsonify({'error': 'Please upload clear ID card photo(face side).'})
