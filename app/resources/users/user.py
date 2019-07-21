from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.extensions import login_manager as login


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    registered_date = db.Column(db.String(120))
    if_verified = db.Column(db.Boolean())
    real_name = db.Column(db.String(120))
    sex = db.Column(db.String(120))
    minority = db.Column(db.String(120))
    account_active = db.Column(db.Boolean())
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    complaints = db.relationship('Complaint', backref='User')
    comments = db.relationship('Comment', backref='User')

    def __init__(self, username, sex, registered_date):
        self.username = username
        self.sex = sex
        self.registered_date = registered_date

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
