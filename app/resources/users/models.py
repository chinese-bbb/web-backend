# from flask_user import UserMixin
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.extensions import login_manager as login
from app.resources.auth.models import EnumGender
from app.resources.comments.models import Comment
from app.resources.complaints.models import Complaint


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    account_active = db.Column(db.Boolean())
    if_verified = db.Column(db.Boolean())
    minority = db.Column(db.String(120))
    real_name = db.Column(db.String(120))
    registered_date = db.Column(db.String(120))
    sex = db.Column(db.Enum(EnumGender), nullable=False)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120), nullable=False)
    is_founder = db.Column(db.Boolean())
    urole = db.Column(db.String(140), default='normal')

    complaints = db.relationship(Complaint, backref='User')
    comments = db.relationship(Comment, backref='User')

    # Define the relationship to Role via UserRoles
    # flask_user required schema change
    roles = db.relationship('Role', secondary='user_roles')
    password = db.Column(db.String(128))

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

    def get_urole(self):
        return self.urole


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
