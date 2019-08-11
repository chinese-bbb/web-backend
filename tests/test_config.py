import os
from copy import deepcopy


def test_testing_config(app):
    old_config = deepcopy(app.config)
    app.config.from_object('config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config['SQLALCHEMY_DATABASE_URI']

    # recover the flask config
    app.config = old_config


def test_development_config(app):
    old_config = deepcopy(app.config)
    app.config.from_object('config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI']

    # recover the flask config
    app.config = old_config


def test_production_config(app):
    old_config = deepcopy(app.config)
    app.config.from_object('config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')

    # recover the flask config
    app.config = old_config
