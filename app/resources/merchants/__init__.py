"""
Merchant module
============
"""
from app.extensions import api


def init_app(app, **kwargs):
    # pylint: disable=unused-argument,unused-variable

    # Touch underlying modules
    from . import models, routes  # noqa

    api.add_namespace(routes.ns)