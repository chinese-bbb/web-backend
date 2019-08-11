import pytest
from flask import session


def test_login(client, auth):
    with client:
        # test that successful login redirects to the index page
        response = auth.login()

        # login request set the user_id in the session
        # check that the user is loaded from the session

        assert response.status_code == 200
        assert session['user_id'] == '1'


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('a', 'test', b'{\n  "error": "Invalid phone num or password"\n}\n'),
        ('test', 'a', b'{\n  "error": "Invalid phone num or password"\n}\n'),
    ),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        resp = auth.logout()
        assert resp.status_code == 200
        assert 'user_id' not in session
