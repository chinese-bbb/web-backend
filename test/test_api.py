import unittest
import json
import os

from app import application

TEST_BASE_URL = 'http://0.0.0.0:5000/'
DOC_URL= '{}/doc/'.format(TEST_BASE_URL)
LOGIN_URL= '{}/api/login'.format(TEST_BASE_URL)
CREATE_COMMENT_URL= '{}/api/comment'.format(TEST_BASE_URL)
MVC_COMMENT_URL= '{}/api/comment/'.format(TEST_BASE_URL)
FETCH_ALL_COMMENT_URL= '{}/api/commentsByComplaint/'.format(TEST_BASE_URL)
CREATE_COMPLAINT_URL= '{}/api/complaint'.format(TEST_BASE_URL)
MVC_COMPLAINT_URL= '{}/api/complaint/'.format(TEST_BASE_URL)
FETCH_COMPLAINTS_BY_USER_URL= '{}/api/complaintByUser'.format(TEST_BASE_URL)

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

    def test_comment(self):
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

    def test_fetch_all_comment(self):
        comment = {"text": "testtesttest1", "complaint_id": 5}
        response = self.app.post(CREATE_COMMENT_URL,
                                 data = json.dumps(comment),
                                 content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"state": "Success"})

        comment = {"text": "testtesttest2", "complaint_id": 5}
        response = self.app.post(CREATE_COMMENT_URL,
                                 data = json.dumps(comment),
                                 content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"state": "Success"})

        ##########################
        # Test fetch all comments
        ##########################
        response = self.app.get(FETCH_ALL_COMMENT_URL + '5',
                                 content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        # Delete all inserted comments.
        response = self.app.delete(MVC_COMMENT_URL + '1')
        self.assertEqual(response.status_code, 204)

        response = self.app.delete(MVC_COMMENT_URL + '2')
        self.assertEqual(response.status_code, 204)


    def test_complaint(self):

        # # Test create a comment
        # complaint1 = {
        #               "merchant_id": 1,
        #               "complaint_body": "122's complain1",
        #               "expected_solution_body": "string",
        #               "complain_type": "type5",
        #               "if_negotiated_by_merchant": True,
        #               "negotiate_timestamp": "2019-06-07T19:12:44.468Z",
        #               "allow_public": True,
        #               "allow_contact_by_merchant": True,
        #               "allow_press": True,
        #               "item_price": "string",
        #               "item_model": "string",
        #               "trade_info": "string",
        #               "relatedProducts": "string",
        #               "purchase_timestamp": "2019-06-07T19:12:44.468Z",
        #               "id_files": [
        #                 {
        #                   "id": 0,
        #                   "s3_path": "string"
        #                 }
        #               ]
        #             }
        #
        # complaint2 = {
        #               "merchant_id": 1,
        #               "complaint_body": "144's complain2",
        #               "expected_solution_body": "string",
        #               "complain_type": "type5",
        #               "if_negotiated_by_merchant": False,
        #               "negotiate_timestamp": "2019-06-07T19:12:44.468Z",
        #               "allow_public": False,
        #               "allow_contact_by_merchant": False,
        #               "allow_press": False,
        #               "item_price": "string",
        #               "item_model": "string",
        #               "trade_info": "string",
        #               "relatedProducts": "string",
        #               "purchase_timestamp": "2019-06-07T19:12:44.468Z",
        #               "invoice_files": [
        #                 {
        #                   "id": 0,
        #                   "s3_path": "string"
        #                 }
        #               ]
        #             }
        #
        # response = self.app.post(CREATE_COMPLAINT_URL,
        #                          data = json.dumps(complaint1),
        #                          content_type='application/json')
        # data = json.loads(response.get_data())
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(data, {"state": "Success"})
        #
        # response = self.app.post(CREATE_COMPLAINT_URL,
        #                          data = json.dumps(complaint2),
        #                          content_type='application/json')
        # data = json.loads(response.get_data())
        # self.assertEqual(response.status_code, 200)
        #
        #

        # Test Get a complaint
        response = self.app.get(MVC_COMPLAINT_URL + '2')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['complaint_id'], '2')

        # Test get all complaints given a user_id
        response = self.app.get(FETCH_COMPLAINTS_BY_USER_URL,
                                query_string=dict(phone_num='13333333333'))
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

