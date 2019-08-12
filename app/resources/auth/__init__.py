"""
Auth module
============
"""


def init_app(app, api, **kwargs):
    # pylint: disable=unused-argument,unused-variable

    # Touch underlying modules
    from . import models, routes  # noqa

    api.register_blueprint(routes.bp)
