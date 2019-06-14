from datetime import datetime
from app import application, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

ma = Marshmallow(application)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    registered_date = db.Column(db.String(120))
    if_verified = db.Column(db.Boolean())
    real_name = db.Column(db.String(120))
    sex       = db.Column(db.String(120))
    minority  = db.Column(db.String(120))
    account_active  = db.Column(db.Boolean())

    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username):
        self.username = username

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


class UserSchema(ma.Schema):
    class Meta:
        model = User
        # Fields to expose
        fields = ("username",
                  "email",
                  "registered_date",
                  "if_verified",
                  "real_name",
                  "sex",
                  "minority",
                  "account_active")


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class FuzzySearchRaw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(140))
    storage = db.Column(db.String(10000))

    def __init__(self, keyword):
        self.keyword = keyword

    def set_storage(self, storage):
        self.storage = storage

    def get_storage(self):
        return self.storage

    def __repr__(self):
        return '<MerchantRaw {}>'.format(self.keyword)


class MerchantQueryRaw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(140))
    storage = db.Column(db.String(20000))

    def __init__(self, keyword):
        self.keyword = keyword

    def set_storage(self, storage):
        self.storage = storage

    def get_storage(self):
        return self.storage

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<MerchantRaw {}>'.format(self.keyword)


