import flask
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from app import application, db, api
from app.models import User, FuzzySearchRaw, MerchantQueryRaw
from app.sms.send_sms import send_message
from app.qichacha.qichacha_api import fuzzy_search, basic_detail
from flask_restplus import Resource, fields
import datetime
import json

from app.utils import text_from_bits, text_to_bits
ns = api.namespace('api', description='Login Module')

@ns.route('/testLogin')
class TestLogin(Resource):
    '''Only Logged in user can see this page'''

    @login_required
    def get(self):
        return {"state": "Success"},200


@ns.route('/phone_exist/<string:phone_num>')
@api.doc(params={'phone_num': 'A phone number'})
class PhoneExist(Resource):
    '''Check if phone number is registered'''

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error'
    })
    def get(self, phone_num):
        user = User.query.filter_by(username=phone_num).first()
        print(user)
        if user is None:
            return {
                phone_num : "Not Registerred phone num"
            },400
        return {"state": "Success"},200

sms_parser = api.parser()
sms_parser.add_argument('v_code', type=str, required=True, help='verification code', location='json')

@ns.route('/sms/<string:phone_num>')
@api.doc(params={'phone_num': 'A phone number'})
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error',
    401: 'Passcode is not correct'
})
class SMS(Resource):

    def get(self, phone_num):
        '''Get verification code for a phone number'''
        log = send_message(phone_num)
        return {"send_log":log},200

    @api.doc(parser=sms_parser)
    def post(self, phone_num):
        '''Verify the verification number'''
        args = sms_parser.parse_args()
        v_code = args['v_code']

        if v_code != '9273':
            return {"error" : "verification code is not correct"}, 401
        return {"state": "Success"},200


login_parser = api.parser()
login_parser.add_argument('phone_num', type=str, required=True, help='Phone Number', location='json')
login_parser.add_argument('password',  type=str, required=True, help='password', location='json')

@ns.route('/login')
@api.doc(responses={
    200: 'Success',
    401: 'Invalid password',
    404: 'User Cannot be found',
    400: 'Validation Error'
})
class Login(Resource):

    @api.doc(parser=login_parser)
    def post(self):
        '''Log in'''
        args = login_parser.parse_args()
        username = args['phone_num']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        print(user)
        if user is None:
            return {
                "error": "User cannot be found"
            }, 404

        if not user.check_password(password):
            print("Invalid username or password")
            return {
                "error": "Invalid phone num or password"
            }, 401

        login_user(user, remember=True)
        return flask.jsonify("OK")

@ns.route('/logout')
@api.doc(responses={
    200: 'Success'
})
class Login(Resource):

    @login_required
    def post(self):
        '''Log out'''
        logout_user()
        return {"state": "Success"},200


register_parser = api.parser()
register_parser.add_argument('phone_num', type=str, required=True, help='Phone Number', location='json')
register_parser.add_argument('password',  type=str, required=True, help='password', location='json')
register_parser.add_argument('sex',       type=str, required=True, help='sex', location='json')

@ns.route('/register')
@api.doc(responses={
    200: 'Register Success',
    400: 'Validation Error'
})
class Register(Resource):

    @api.doc(parser=register_parser)
    def post(self):
        '''Register'''

        args = register_parser.parse_args()
        username = args['phone_num']
        password = args['password']
        sex      = args['sex']

        today = datetime.date.today()
        user = User(username=username, sex=sex, registered_date=today)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        return {"state": "Success"},200


changepwd_parser = api.parser()
changepwd_parser.add_argument('phone_num', type=str, required=True, help='Phone Number', location='json')
changepwd_parser.add_argument('old_password',  type=str, required=True, help='password', location='json')
changepwd_parser.add_argument('new_password',  type=str, required=True, help='password', location='json')

@ns.route('/changepw')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class ChangePassword(Resource):

    @api.doc(parser=changepwd_parser)
    def post(self):
        '''Change Password'''

        args = changepwd_parser.parse_args()
        username = args['phone_num']
        old_password = args['old_password']
        new_password = args['new_password']

        user = User.query.filter_by(username=username).first()
        print(user)
        if user is None or not user.check_password(old_password):
            print("Invalid username or password")
            return flask.jsonify({
                "error": "Invalid phone num or password"
            })

        user.set_password(new_password)
        db.session.commit()
        flash('Congratulations, successfully updated user password!')
        return flask.jsonify("OK")


qichacha_parser = api.parser()
qichacha_parser.add_argument('keyword', type=str, required=True, help='keyword', location='json')

@ns.route('/fuzzy_query')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class FuzzyQuery(Resource):

    @login_required
    @api.doc(parser=qichacha_parser)
    def post(self):
        '''fuzzy_query'''

        args = qichacha_parser.parse_args()
        keyword = args['keyword']

        fuzzy_search_res = FuzzySearchRaw.query.filter_by(keyword=keyword).first()
        if fuzzy_search_res is None:
            fuzzy_result_json_dict = fuzzy_search(keyword)
            fuzzy_result_json_str = json.dumps(fuzzy_result_json_dict)

            search_content = FuzzySearchRaw(keyword=keyword)
            search_content.set_storage(fuzzy_result_json_str)
            db.session.add(search_content)
            db.session.commit()

            return {"return": fuzzy_result_json_str}
        else:
            storage = fuzzy_search_res.get_storage()
            print("has storage")
            return {"return": storage}


@ns.route('/merchant_query')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class MerchantQuery(Resource):

    @login_required
    @api.doc(parser=qichacha_parser)
    def post(self):
        '''fuzzy_query'''

        args = qichacha_parser.parse_args()
        keyword = args['keyword']

        merchant_query_res = MerchantQueryRaw.query.filter_by(keyword=keyword).first()
        if merchant_query_res is None:
            merchant_json_dict = basic_detail(keyword)
            merchant_json_str = json.dumps(merchant_json_dict)

            search_content = MerchantQueryRaw(keyword=keyword)
            search_content.set_storage(merchant_json_str)
            db.session.add(search_content)
            db.session.commit()

            return {"return": merchant_json_str}
        else:
            storage = merchant_query_res.get_storage()
            print("has merchant query storage")
            return {"return": storage}
