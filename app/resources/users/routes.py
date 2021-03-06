import logging

from flask.views import MethodView
from flask_user import current_user
from flask_user import login_required

from .models import User
from .schemas import ChangePasswordParameters
from .schemas import UserSchema
from app.extensions import db
from flask_rest_api import Blueprint

log = logging.getLogger(__name__)

bp = Blueprint('users', 'users', url_prefix='/users', description='User Resources API')


@bp.route('/me')
class UserMe(MethodView):
    """
    Only Logged in user can see this page.
    """

    @login_required
    @bp.response(UserSchema)
    def get(self):
        log.debug('fetching user <%s>\'s profile', current_user.username)
        return User.query.get_or_404(current_user.id)


@bp.route('/changepw')
class ChangePassword(MethodView):
    @bp.arguments(ChangePasswordParameters)
    def post(self, args):
        """
        Change Password.
        """

        username = args['phone_num']
        old_password = args['old_password']
        new_password = args['new_password']

        log.debug('trying to change user <%s>\'s password', username)

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(old_password):
            log.debug('Invalid username or password')
            return {'error': 'Invalid phone num or password'}

        user.set_password(new_password)
        db.session.commit()
        return 'OK'
