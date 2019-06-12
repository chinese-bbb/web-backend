import unittest
import json
import os

from app import application

TEST_BASE_URL = 'http://0.0.0.0:5000/'
DOC_URL= '{}/doc/'.format(TEST_BASE_URL)
LOGIN_URL= '{}/api/login'.format(TEST_BASE_URL)

class TestHuxinAppLocalhost(unittest.TestCase):

    def setUp(self):
        self.app = application.test_client()
        self.app.testing = True

    def test_get_doc_page(self):
        response = self.app.get(DOC_URL)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        user = {"phone_num": "13333333333", "password": "Abcd3333"}
        response = self.app.post(LOGIN_URL,
                                 data = json.dumps(user),
                                 content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, "OK")


    def tearDown(self):
        # reset app.items to initial state
        # application.items = self.backup_items
        print("unit test finished.")
