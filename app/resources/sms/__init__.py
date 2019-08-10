"""
Auth module
============
"""
from app.extensions import api


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable

    # Touch underlying modules
    from . import routes  # noqa

    api.register_blueprint(routes.bp)
