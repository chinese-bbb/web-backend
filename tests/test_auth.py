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


@pytest.mark.parametrize(
    ('phone_num',),
    (('13312341234',), ('+8613312341234',), ('13312345678',), ('+8613312345678',)),
)
def test_invalid_register(client, phone_num):
    with client:
        client.set_cookie('localhost', key='phone_auth', value='yse')
        response = client.post(
            '/api/auth/register',
            json={
                'phone_num': phone_num,
                'sex': 'male',
                'password': 'abcd1234',
                'first_name': '',
                'last_name': 'he',
                'email': 'ghost@example.com',
            },
        )
        assert response.status_code == 422
        assert 'user_id' not in session


def test_valid_register(client):
    with client:
        client.set_cookie('localhost', key='phone_auth', value='yse')
        response = client.post(
            '/api/auth/register',
            json={
                'phone_num': '+8613333333334',
                'sex': 'male',
                'password': 'abcd1234',
                'first_name': '',
                'last_name': 'he',
                'email': 'ghost@example.com',
            },
        )
        assert response.status_code == 200
        assert 'user_id' in session
