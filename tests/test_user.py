from flask import session
from flask.testing import FlaskClient


def test_get_me_not_loggedin(client: FlaskClient, auth):
    resp = client.get('/api/users/me')

    # TODO: needs to be better tuned up
    assert resp.status_code == 302


def test_get_me(client, auth):
    with client:
        auth.login()
        resp = client.get('/api/users/me')
        assert resp.status_code == 200
        assert 'user_id' in session
