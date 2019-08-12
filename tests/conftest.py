import os
import tempfile

from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from dotenv import find_dotenv
from dotenv import load_dotenv
from flask import Flask
from flask.testing import FlaskClient
from pytest import fixture
from pytest import yield_fixture

from app import create_app
from app.extensions import db as _db
from app.extensions import SQLAlchemy

load_dotenv(find_dotenv())

# read in SQL for populating test data
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


# def pytest_configure(config):
#     sys._called_from_test = True
# def pytest_unconfigure(config):
#     del sys._called_from_test


@fixture(scope='session')
def app():
    db_fd, db_path = tempfile.mkstemp()

    # if you want to debug the db file in file system uncomment the statement below
    os.environ['DATABASE_URL'] = 'sqlite:///' + db_path

    _app = create_app('Testing API', 'config.TestingConfig')

    if _app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:':
        print('\n========== Using sqlite memory db ==========')
    else:
        print('\n===== Testing db path:', db_path)

    print('\n----- CREATE FLASK APPLICATION')

    ctx = _app.app_context()
    ctx.push()
    print('\n----- CREATE FLASK APPLICATION CONTEXT')

    yield _app

    ctx.pop()
    print('\n----- RELEASE FLASK APPLICATION CONTEXT')

    os.close(db_fd)
    os.unlink(db_path)


@fixture(scope='session')
def client(app: Flask):
    return app.test_client()


@fixture(scope='session')
def runner(app: Flask):
    return app.test_cli_runner()


def apply_migration():
    config = AlembicConfig('../migrations/alembic.ini')
    config.set_main_option('script_location', '../migrations')
    alembic_upgrade(config, 'head')


# todo: try to use https://github.com/jeancochrane/pytest-flask-sqlalchemy later
@yield_fixture(scope='session')
def db(app: Flask):
    _db.app = app
    _db.create_all()

    # add predefined test data to test db
    raw_conn = _db.engine.raw_connection()
    cursor = raw_conn.cursor()
    cursor.executescript(_data_sql)
    raw_conn.close()

    yield _db

    _db.drop_all()
    print('\n----- RELEASE TEST DB CONNECTION POOL')


@fixture(scope='function', autouse=True)
def session(db: SQLAlchemy):
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)
    print('\n----- CREATE DB SESSION')

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()
    print('\n----- ROLLBACK DB SESSION')


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='13312341234', password='Abcd3333'):
        return self._client.post(
            '/api/auth/login', json={'phone_num': username, 'password': password}
        )

    def logout(self):
        return self._client.post('/api/auth/logout')


@fixture(scope='function', autouse=True)
def auth(client: FlaskClient):
    return AuthActions(client)
