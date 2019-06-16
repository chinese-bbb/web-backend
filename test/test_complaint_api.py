import json
import unittest

from test.test_base import BaseTestClass, TEST_BASE_URL

CREATE_COMPLAINT_URL = '{}/api/complaint'.format(TEST_BASE_URL)
MVC_COMPLAINT_URL = '{}/api/complaint/'.format(TEST_BASE_URL)
FETCH_COMPLAINTS_BY_USER_URL = '{}/api/complaintByUser'.format(TEST_BASE_URL)
FETCH_COMPLAINTS_BY_MERCHANT_URL = '{}/api/complaintByMerchant'.format(TEST_BASE_URL)


class TestComplaintAPI(BaseTestClass):
    def setUp(self):
        super().setUp()

    @unittest.skip
    def test_complaint(self):
        # # Test create a comment
        complaint1 = {
            "merchant_id": 1,
            "complaint_body": "eeeeeeees complain1",
            "expected_solution_body": "string",
            "complain_type": "type5",
            "if_negotiated_by_merchant": True,
            "negotiate_timestamp": "2019-06-07T19:12:44.468Z",
            "allow_public": True,
            "allow_contact_by_merchant": True,
            "allow_press": True,
            "item_price": "string",
            "item_model": "string",
            "trade_info": "string",
            "relatedProducts": "string",
            "purchase_timestamp": "2019-06-07T19:12:44.468Z",
            "evidence_files": [
                {
                    "s3_path": "string1"
                }
            ]
        }

        complaint2 = {
            "merchant_id": 1,
            "complaint_body": "bbbbbbbbbb's complain2",
            "expected_solution_body": "string",
            "complain_type": "type5",
            "if_negotiated_by_merchant": False,
            "negotiate_timestamp": "2019-06-07T19:12:44.468Z",
            "allow_public": False,
            "allow_contact_by_merchant": False,
            "allow_press": False,
            "item_price": "string",
            "item_model": "string",
            "trade_info": "string",
            "relatedProducts": "string",
            "purchase_timestamp": "2019-06-07T19:12:44.468Z",
            "invoice_files": [
                {
                    "s3_path": "string2"
                }
            ]
        }

        response = self.app.post(CREATE_COMPLAINT_URL,
                                 data=json.dumps(complaint1),
                                 content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {"state": "Success"})

        response = self.app.post(CREATE_COMPLAINT_URL,
                                 data=json.dumps(complaint2),
                                 content_type='application/json')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)

        # Test Get a complaint
        response = self.app.get(MVC_COMPLAINT_URL + '2')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['complaint_id'], '2')

        # Test get all complaints given a user_id
        response = self.app.get(FETCH_COMPLAINTS_BY_USER_URL,
                                query_string=dict(phone_num='az'))
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        # Test get all complaints given a merchant_id
        response = self.app.get(FETCH_COMPLAINTS_BY_MERCHANT_URL,
                                query_string=dict(merchant_id='1'))
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        # Test delete complaints
        response = self.app.delete(MVC_COMPLAINT_URL + '2')
        self.assertEqual(response.status_code, 204)
        response = self.app.delete(MVC_COMPLAINT_URL + '1')
        self.assertEqual(response.status_code, 204)
