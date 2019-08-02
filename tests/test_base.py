# base_test_class.py
import json
from unittest import TestCase

from app import application

TEST_BASE_URL = 'http://0.0.0.0:5000/'
LOGIN_URL = '{}/api/login'.format(TEST_BASE_URL)


class BaseTestClass(TestCase):
    """Base test class for the two components."""

    __test__ = False  # important, makes sure tests are not run on base class

    component = None

    def setUp(self):
        self.app = application.test_client()
        self.app.testing = True
        user = {'phone_num': '13333333333', 'password': 'Abcd3333'}
        self.app.post(LOGIN_URL, data=json.dumps(user), content_type='application/json')
