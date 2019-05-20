import flask
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import application, db, api
from app.forms import LoginForm, RegistrationForm, LoginInputs, PhoneNumInputs, PhoneVeifyInputs
from app.models import User
from app.sms.send_sms import send_message
from flask_restplus import Resource, fields
import datetime

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
sms_parser.add_argument('v_code', type=str, required=True, help='verification code', location='form')

@ns.route('/sms/<string:phone_num>')
@api.doc(params={'phone_num': 'A phone number'})
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
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
            return {"error" : "verification code is not correct"}, 400
        return flask.jsonify("OK"),200


login_parser = api.parser()
login_parser.add_argument('phone_num', type=str, required=True, help='Phone Number', location='form')
login_parser.add_argument('password',  type=str, required=True, help='password', location='form')

@ns.route('/login')
@api.doc(responses={
    200: 'Success',
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
        if user is None or not user.check_password(password):
            print("Invalid username or password")
            return flask.jsonify({
                "error": "Invalid phone num or password"
            })
        login_user(user, remember=True)
        return flask.jsonify("OK")


register_parser = api.parser()
register_parser.add_argument('phone_num', type=str, required=True, help='Phone Number', location='form')
register_parser.add_argument('password',  type=str, required=True, help='password', location='form')
register_parser.add_argument('sex',       type=str, required=True, help='sex', location='form')

@ns.route('/register')
@api.doc(responses={
    200: 'Success',
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

        return flask.jsonify("OK")


changepwd_parser = api.parser()
changepwd_parser.add_argument('phone_num', type=str, required=True, help='Phone Number', location='form')
changepwd_parser.add_argument('old_password',  type=str, required=True, help='password', location='form')
changepwd_parser.add_argument('new_password',  type=str, required=True, help='password', location='form')


@ns.route('/changepw')
@api.doc(responses={
    200: 'Success',
    400: 'Validation Error'
})
class ChangePassword(Resource):

    @api.doc(parser=changepwd_parser)
    def post(self):
        '''Register'''

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
