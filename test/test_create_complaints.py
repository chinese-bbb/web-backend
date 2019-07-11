import json
from test.test_base import BaseTestClass
from test.test_base import TEST_BASE_URL

CREATE_COMPLAINT_URL = '{}/api/complaint'.format(TEST_BASE_URL)
MVC_COMPLAINT_URL = '{}/api/complaint/'.format(TEST_BASE_URL)
FETCH_COMPLAINTS_BY_USER_URL = '{}/api/complaintByUser'.format(TEST_BASE_URL)
FETCH_COMPLAINTS_BY_MERCHANT_URL = '{}/api/complaintByMerchant'.format(TEST_BASE_URL)


class TestComplaintAPI(BaseTestClass):
    def setUp(self):
        super().setUp()

    def test_complaint(self):
        # # Test create a comment
        complaint1 = {
            'merchant_id': 1,
            'complaint_body': 'eeeeeeees complain1',
            'expected_solution_body': 'string',
            'complain_type': 'type5',
            'if_negotiated_by_merchant': True,
            'negotiate_timestamp': '2019-06-07T19:12:44.468Z',
            'allow_public': True,
            'allow_contact_by_merchant': True,
            'allow_press': True,
            'item_price': 'string',
            'item_model': 'string',
            'trade_info': 'string',
            'relatedProducts': 'string',
            'purchase_timestamp': '2019-06-07T19:12:44.468Z',
            'evidence_files': [{'s3_path': 'string1'}],
        }

        complaint2 = {
            'merchant_id': 1,
            'complaint_body': "bbbbbbbbbb's complain2",
            'expected_solution_body': 'string',
            'complain_type': 'type5',
            'if_negotiated_by_merchant': False,
            'negotiate_timestamp': '2019-06-07T19:12:44.468Z',
            'allow_public': False,
            'allow_contact_by_merchant': False,
            'allow_press': False,
            'item_price': 'string',
            'item_model': 'string',
            'trade_info': 'string',
            'relatedProducts': 'string',
            'purchase_timestamp': '2019-06-07T19:12:44.468Z',
            'invoice_files': [{'s3_path': 'string2'}],
        }

        complaint3 = {
            'merchant_id': 2,
            'complaint_body': 'eeeeeeees complain1',
            'expected_solution_body': 'string',
            'complain_type': 'type5',
            'if_negotiated_by_merchant': True,
            'negotiate_timestamp': '2019-06-07T19:12:44.468Z',
            'allow_public': True,
            'allow_contact_by_merchant': True,
            'allow_press': True,
            'item_price': 'string',
            'item_model': 'string',
            'trade_info': 'string',
            'relatedProducts': 'string',
            'purchase_timestamp': '2019-06-07T19:12:44.468Z',
            'evidence_files': [{'s3_path': 'string1'}],
        }

        complaint4 = {
            'merchant_id': 2,
            'complaint_body': "bbbbbbbbbb's complain2",
            'expected_solution_body': 'string',
            'complain_type': 'type5',
            'if_negotiated_by_merchant': False,
            'negotiate_timestamp': '2019-06-07T19:12:44.468Z',
            'allow_public': False,
            'allow_contact_by_merchant': False,
            'allow_press': False,
            'item_price': 'string',
            'item_model': 'string',
            'trade_info': 'string',
            'relatedProducts': 'string',
            'purchase_timestamp': '2019-06-07T19:12:44.468Z',
            'invoice_files': [{'s3_path': 'string2'}],
        }

        complaint5 = {
            'merchant_id': 3,
            'complaint_body': 'eeeeeeees complain1',
            'expected_solution_body': 'string',
            'complain_type': 'type5',
            'if_negotiated_by_merchant': True,
            'negotiate_timestamp': '2019-06-07T19:12:44.468Z',
            'allow_public': True,
            'allow_contact_by_merchant': True,
            'allow_press': True,
            'item_price': 'string',
            'item_model': 'string',
            'trade_info': 'string',
            'relatedProducts': 'string',
            'purchase_timestamp': '2019-06-07T19:12:44.468Z',
            'evidence_files': [{'s3_path': 'string1'}],
        }

        complaint6 = {
            'merchant_id': 3,
            'complaint_body': "bbbbbbbbbb's complain2",
            'expected_solution_body': 'string',
            'complain_type': 'type5',
            'if_negotiated_by_merchant': False,
            'negotiate_timestamp': '2019-06-07T19:12:44.468Z',
            'allow_public': False,
            'allow_contact_by_merchant': False,
            'allow_press': False,
            'item_price': 'string',
            'item_model': 'string',
            'trade_info': 'string',
            'relatedProducts': 'string',
            'purchase_timestamp': '2019-06-07T19:12:44.468Z',
            'invoice_files': [{'s3_path': 'string2'}],
        }

        self.app.post(
            CREATE_COMPLAINT_URL,
            data=json.dumps(complaint1),
            content_type='application/json',
        )
        self.app.post(
            CREATE_COMPLAINT_URL,
            data=json.dumps(complaint2),
            content_type='application/json',
        )
        self.app.post(
            CREATE_COMPLAINT_URL,
            data=json.dumps(complaint3),
            content_type='application/json',
        )
        self.app.post(
            CREATE_COMPLAINT_URL,
            data=json.dumps(complaint4),
            content_type='application/json',
        )
        self.app.post(
            CREATE_COMPLAINT_URL,
            data=json.dumps(complaint5),
            content_type='application/json',
        )
        self.app.post(
            CREATE_COMPLAINT_URL,
            data=json.dumps(complaint6),
            content_type='application/json',
        )
