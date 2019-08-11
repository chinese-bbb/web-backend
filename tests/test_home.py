from flask.testing import FlaskClient


def test_home(client: FlaskClient):
    resp = client.get('/')
    data = resp.data.decode('utf-8')
    assert resp.status_code == 200
    assert 'Hi, welcome to visit our RESTful api service' in data
    assert 'version: local' in data
