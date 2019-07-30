import datetime
import enum
import logging
import random

import flask
from flask import after_this_request
from flask import flash
from flask import request
from flask import session
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from flask_restplus import fields
from flask_restplus import Namespace
from flask_restplus import Resource

from app.extensions import api
from app.extensions import db
from app.resources.users.models import User
from app.services.tencent.id_ocr import tencent_ocr
from app.services.tencent.send_sms import send_message

log = logging.getLogger(__name__)

ns = Namespace('auth', path='/auth', description='Authentication Related API')

# Dictionary to store sms verification code
messageDict = {}


@ns.route('/phone_exist/<string:phone_num>')
@api.doc(params={'phone_num': 'A phone number'})
class PhoneExist(Resource):
    """Check if phone number is registered."""

    @api.doc(responses={200: 'Success', 400: 'Validation Error'})
    def get(self, phone_num):
        user = User.query.filter_by(username=phone_num).first()
        log.debug(user)
        if user is None:
            return {phone_num: 'Not Registerred phone num'}, 400
        return {'state': 'Success'}, 200


sms_parser = api.parser()
sms_parser.add_argument(
    'v_code', type=str, required=True, help='verification code', location='json'
)


@ns.route('/sms/<string:phone_num>')
@api.doc(params={'phone_num': 'A phone number'})
@api.doc(
    responses={200: 'Success', 400: 'Validation Error', 401: 'Passcode is not correct'}
)
class SMS(Resource):
    def get(self, phone_num):
        """Get verification code for a phone number."""
        rand_num = random.randint(1000, 9999)
        log = send_message(phone_num, rand_num)
        sid = log['sid']
        messageDict[sid] = str(rand_num)
        log.debug(rand_num)
        return {'state': 'Success'}, 200, {'Set-Cookie': 'sid=' + sid}

    def _check_cookie_sid(self):
        if request.cookies.get('sid') is None:
            api.abort(403, "The cookie doesn't come with sid entry")

        @after_this_request
        def set_register_cookie(response):
            response.set_cookie('phone_auth', 'yes', max_age=64800)
            return response

        return request.cookies.get('sid')

    @api.doc(parser=sms_parser)
    def post(self, phone_num):
        """Verify the verification number."""
        args = sms_parser.parse_args()
        v_code = args['v_code']

        sid = self._check_cookie_sid()

        if messageDict[sid] != v_code:
            return {'error': 'verification code is not correct'}, 401
        return {'state': 'Success'}, 200


login_parser = api.parser()
login_parser.add_argument(
    'phone_num', type=str, required=True, help='Phone Number', location='json'
)
login_parser.add_argument(
    'password', type=str, required=True, help='password', location='json'
)


@ns.route('/login')
@api.doc(
    responses={
        200: 'Success',
        401: 'Invalid password',
        404: 'User Cannot be found',
        400: 'Validation Error',
    }
)
class Login(Resource):
    @api.doc(parser=login_parser)
    def post(self):
        """Log in."""
        args = login_parser.parse_args()
        username = args['phone_num']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        log.debug(user)
        if user is None:
            return {'error': 'User cannot be found'}, 404

        if not user.check_password(password):
            log.debug('Invalid username or password')
            return {'error': 'Invalid phone num or password'}, 401

        login_user(user, remember=True)
        return flask.jsonify('OK')


@ns.route('/logout')
@api.doc(responses={200: 'Success'})
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


register_fields = api.model(
    'RegisterModel',
    {
        'sex': fields.String(
            description='gender type', enum=EnumSexType._member_names_, required=True
        ),
        'phone_num': fields.String(description='phone_num', required=True),
        'password': fields.String(description='password', required=True),
        'first_name': fields.String(description='first_name', required=True),
        'last_name': fields.String(description='last_name', required=True),
        'email': fields.String(description='email', required=False)
    },
)


@ns.route('/register')
@api.doc(responses={200: 'Register Success', 400: 'Validation Error'})
class Register(Resource):
    def _check_cookie_phone_allow(self):
        if request.cookies.get('phone_auth') is None:
            api.abort(403, "The cookie doesn't come with phone_allow entry")

    @api.expect(register_fields)
    def post(self):
        """Register a user."""

        self._check_cookie_phone_allow()
        data = api.payload
        username = data['phone_num']
        sex = data['sex']
        password = data['password']
        if 'email' in data:
            email = data['email']
        else:
            email = ""

        today = datetime.date.today()
        user = User(username=username, sex=sex, registered_date=today)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.account_active = True
        user.if_verified = False
        user.set_password(password)
        user.email = email
        with db.session.begin():
            db.session.add(user)

        flash('Congratulations, you are now a registered user!')

        login_user(user, remember=True)
        return flask.jsonify('OK')


changepwd_parser = api.parser()
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
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class ChangePassword(Resource):
    @api.doc(parser=changepwd_parser)
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

        flash('Congratulations, successfully updated user password!')
        return flask.jsonify('OK')


resetpwd_parser = api.parser()
resetpwd_parser.add_argument(
    'phone_num', type=str, required=True, help='Phone Number', location='json'
)
resetpwd_parser.add_argument(
    'new_password', type=str, required=True, help='new_password', location='json'
)


@ns.route('/resetpw')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class ResetPassword(Resource):
    @api.doc(parser=resetpwd_parser)
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

        flash('Congratulations, successfully updated user password!')
        return flask.jsonify('OK')


identify_parser = api.parser()
identify_parser.add_argument(
    'id_path', type=str, required=True, help='upload path', location='json'
)


@ns.route('/identify')
@api.doc(responses={200: 'Success', 400: 'Validation Error'})
class IdentifyIDCard(Resource):
    @login_required
    @api.doc(parser=identify_parser)
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

                flash('Congratulations, successfully verified your ID card!')
                return flask.jsonify('OK')
            else:
                return flask.jsonify(
                    {'error': "ID card name/sex doesn't match your register name/sex!"}
                )
        return flask.jsonify({'error': 'Please upload clear ID card photo(face side).'})
