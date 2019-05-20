import flask
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import application, db
from app.forms import LoginForm, RegistrationForm, LoginInputs, PhoneNumInputs, PhoneVeifyInputs
from app.models import User
from flasgger import swag_from
from app.sms.send_sms import send_message

@application.route('/')
@application.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@application.route('/phone_exist', methods=['GET'])
@swag_from('spec_phone.yml')
def exist():
    print(request.form)
    inputs = PhoneNumInputs(request)
    if not inputs.validate():
        return flask.jsonify(success=False, errors=inputs.errors)

    username = request.form['phonenum']

    user = User.query.filter_by(username=username).first()
    print(user)
    if user is None:
        return flask.jsonify(error=401, text ={
            "error" : "Not Registerred phone num"
        })
    return flask.jsonify("OK")


@application.route('/sms_send', methods=['POST'])
@swag_from('spec_phone.yml')
def sms_send():
    print(request.form)
    inputs = PhoneNumInputs(request)
    if not inputs.validate():
        return flask.jsonify(success=False, errors=inputs.errors)

    phone_num = request.form['phonenum']
    send_message(phone_num)
    return flask.jsonify("OK")

@application.route('/sms_verify', methods=['POST'])
@swag_from('spec_phone_verify.yml')
def sms_verify():
    print(request.form)
    inputs = PhoneVeifyInputs(request)
    if not inputs.validate():
        return flask.jsonify(success=False, errors=inputs.errors)

    v_code    = request.form['vcode']
    if v_code != '9273':
        return flask.jsonify(success=False, errors="verification code is not correct")
    return flask.jsonify("OK")


@application.route('/login', methods=['POST', 'GET'])
@swag_from('spec_login.yml')
def login():
    print(request.form)
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@application.route('/login2', methods=['POST'])
@swag_from('spec_login.yml')
def loginNoForm():
    print(request.form)
    inputs = LoginInputs(request)
    if not inputs.validate():
        return flask.jsonify(success=False, errors=inputs.errors)

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    print(user)
    if user is None or not user.check_password(password):
        print("Invalid username or password")
        return flask.jsonify({
            "error" : "Invalid phone num or password"
        })
    login_user(user, remember=True)
    return flask.jsonify("OK")


@application.route('/logout')
@swag_from('spec_logout.yml')
def logout():
    logout_user()
    return redirect(url_for('index'))


@application.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
