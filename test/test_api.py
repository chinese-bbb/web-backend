import unittest
import json
import os

from app import application

TEST_BASE_URL = 'http://0.0.0.0:5000/'
DOC_URL= '{}/doc/'.format(TEST_BASE_URL)
LOGIN_URL= '{}/api/login'.format(TEST_BASE_URL)
CREATE_COMMENT_URL= '{}/api/comment'.format(TEST_BASE_URL)
MVC_COMMENT_URL= '{}/api/comment/'.format(TEST_BASE_URL)

class TestHuxinAppLocalhost(unittest.TestCase):

    def setUp(self):
        self.app = application.test_client()
        self.app.testing = True
        user = {"phone_num": "13333333333", "password": "Abcd3333"}
        response = self.app.post(LOGIN_URL,
                                 data = json.dumps(user),
                                 content_type='application/json')

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

    def test_comment_comment(self):

        # Test create a comment
        comment = {"text": "testtesttest", "complaint_id": 5}
        response = self.app.post(CREATE_COMMENT_URL,
                                 data = json.dumps(comment),
                                 content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"state": "Success"})


        # Test get a comment
        response = self.app.get(MVC_COMMENT_URL + '1')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['text'], 'testtesttest')
        self.assertEqual(data['user_id'], 6)

        # Test update a comment
        data = {"text": "secondTest"}
        response = self.app.put(MVC_COMMENT_URL + '1',
                                data=json.dumps(data),
                                content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['text'], 'secondTest')
        self.assertEqual(data['user_id'], 6)

        # Test delete a comment
        response = self.app.delete(MVC_COMMENT_URL + '1',
                                   headers={'Content-Type': 'application/x-www-form-urlencoded'})
        self.assertEqual(response.status_code, 204)
