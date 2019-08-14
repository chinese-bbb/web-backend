# encoding: utf-8
"""
Logging adapter with specified role
---------------
"""

from app.extensions import login_manager
from flask_login import current_user
from functools import wraps
from flask import flash


def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):

            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if ((current_user.urole != role) and (role != "ANY")):
                flash("This API cannot accessed due to incorrect role.")
                return login_manager.unauthorized()
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper
