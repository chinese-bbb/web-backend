from .models import User
from app.extensions import db


def save_new_user(data):
    user = User.query.filter_by(username=data['phone_num']).first()
    return user


def get_all_users():
    return User.query.all()


def get_a_user(id):
    return User.query.filter_by(id=id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
