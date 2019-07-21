# encoding: utf-8
"""
Migration adapter
---------------
"""
from flask_migrate import Migrate

from app.extensions import db


def init_app(app, **kwargs):
    migrate = Migrate(app, db)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)

    return migrate
