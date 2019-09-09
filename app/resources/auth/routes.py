import datetime
import logging

import phonenumbers
from flask import abort
from flask import make_response
from flask import request
from flask import session
from flask.views import MethodView
from flask_login import login_user
from flask_login import logout_user
from flask_user import login_required
from phonenumbers import NumberParseException

from .schemas import CheckUserIdentificationParameters
from .schemas import CreateAuthClientParameters
from .schemas import RegisterClientParameters
from .schemas import ResetPasswordParameters
from app.extensions import db
from app.resources.users.models import User
from app.services.tencent.id_ocr import tencent_ocr
from flask_rest_api import Blueprint

log = logging.getLogger(__name__)

bp = Blueprint(
    'auth', 'auth', url_prefix='/auth', description='Authentication Related API'
)


@bp.route('/phone_exist/<phone_num>')
class PhoneExist(MethodView):
    """
    Check if phone number is registered.
    """

    def get(self, phone_num):
        user = User.query.filter_by(username=phone_num).first()

        log.debug('checking if user <%s> exists', phone_num)

        if user is None:
            try:
                result = phonenumbers.parse(phone_num, 'CN')
                if result.country_code == 86:
                    phone_num = result.national_number
                user = User.query.filter_by(username=phone_num).first()
            except NumberParseException:
                return {'error': 'Invalid phone num'}, 404

            if user is None:
                return {phone_num: 'Not Registered phone num'}, 404

        return {'state': 'Success'}


@bp.route('/login')
class Login(MethodView):
    @bp.arguments(CreateAuthClientParameters)
    def post(self, args):
        username = args['phone_num']
        password = args['password']

        log.debug('logging in user: %s', username)

        user = User.query.filter_by(username=username).first()

        if user is None:
            try:
                result = phonenumbers.parse(username, 'CN')
                if result.country_code == 86:
                    username = result.national_number
                user = User.query.filter_by(username=username).first()
            except NumberParseException:
                return {'error': 'Invalid phone num or password'}, 404

            if user is None:
                return {'error': 'Invalid phone num or password'}, 404

        if not user.check_password(password):
            log.debug('Invalid username or password')
            return {'error': 'Invalid phone num or password'}, 404

        login_user(user, remember=True)
        return 'OK'


@bp.route('/logout')
class Logout(MethodView):
    @login_required
    def post(self):
        """
        Log out.
        """
        log.debug('logging out user: %s', session['user_id'])
        logout_user()
        session.clear()
        resp = make_response({'state': 'Success'})
        resp.set_cookie('remember_token', expires=0)
        return resp


@bp.route('/register')
class Register(MethodView):
    def _check_cookie_phone_allow(self):
        if request.cookies.get('phone_auth') is None:
            abort(403, "The cookie doesn't come with phone_allow entry")

    @bp.arguments(RegisterClientParameters)
    def post(self, args):
        """
        Register a user.
        """

        self._check_cookie_phone_allow()
        data = args
        username = data['phone_num']

        log.debug('trying to register user <%s>', username)

        user = User.query.filter_by(username=username).first()

        if user:
            return {'error': 'user already exist'}, 422

        try:
            result = phonenumbers.parse(username, 'CN')
            if '+' + str(result.country_code) + str(result.national_number) != username:
                return {'error': 'Invalid phone num or password'}, 422
            user = User.query.filter_by(username=result.national_number).first()

            if user:
                return {'error': 'user already exist'}, 422
        except NumberParseException:
            return {'error': 'Invalid phone num or password'}, 422

        sex = data['sex']
        password = data['password']

        today = datetime.date.today()
        user = User(username=username, sex=sex, registered_date=today)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.account_active = True
        user.if_verified = False
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)
        return 'OK'


@bp.route('/resetpw')
class ResetPassword(MethodView):
    @bp.arguments(ResetPasswordParameters)
    def post(self, args):
        """
        Reset Password.
        """

        username = args['phone_num']
        new_password = args['new_password']

        user = User.query.filter_by(username=username).first()
        log.debug('trying to reset user <%s>\'s password', username)

        if user is None:
            try:
                result = phonenumbers.parse(username, 'CN')
                if result.country_code == 86:
                    username = result.national_number
                user = User.query.filter_by(username=username).first()
            except NumberParseException:
                return {'error': 'Invalid phone num or password'}, 404

            if user is None:
                log.debug('Invalid username')
                return {'error': 'Invalid phone num'}, 404

        log.debug(user)
        user.set_password(new_password)
        db.session.commit()

        return 'OK'


@bp.route('/identify')
class IdentifyIDCard(MethodView):
    @login_required
    @bp.arguments(CheckUserIdentificationParameters)
    def post(self, args):
        """
        Identify user ID card.
        """
        user_id = session['user_id']
        id_path = args['id_path']
        if not id_path:
            return {'error': 'Invalid image url'}

        # TODO: remove this hack in near future.
        user = User.query.filter_by(id=user_id).first()
        user.if_verified = True
        db.session.commit()

        return 'OK'

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

                return 'OK'
            else:
                return {
                    'error': "ID card name/sex doesn't match your register name/sex!"
                }

        return {'error': 'Please upload clear ID card photo(face side).'}
