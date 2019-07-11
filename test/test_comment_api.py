import json
import unittest
from test.test_base import BaseTestClass
from test.test_base import TEST_BASE_URL

CREATE_COMMENT_URL = '{}/api/comment'.format(TEST_BASE_URL)
MVC_COMMENT_URL = '{}/api/comment/'.format(TEST_BASE_URL)
FETCH_ALL_COMMENT_URL = '{}/api/commentsByComplaint/'.format(TEST_BASE_URL)


class TestCommentAPI(BaseTestClass):
    def setUp(self):
        super().setUp()

    @unittest.skip
    def test_comment(self):
        # Test create a comment
        comment = {'text': 'testtesttest', 'complaint_id': 1}
        response = self.app.post(
            CREATE_COMMENT_URL,
            data=json.dumps(comment),
            content_type='application/json',
        )
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'state': 'Success'})

        # Test get a comment
        response = self.app.get(MVC_COMMENT_URL + '1')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['text'], 'testtesttest')
        self.assertEqual(data['user'] is not None, True)

        # Test update a comment
        data = {'text': 'secondTest'}
        response = self.app.put(
            MVC_COMMENT_URL + '1',
            data=json.dumps(data),
            content_type='application/json',
        )
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['text'], 'secondTest')
        self.assertEqual(data['user'] is not None, True)

        # Test delete a comment
        response = self.app.delete(
            MVC_COMMENT_URL + '1',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        self.assertEqual(response.status_code, 204)

    # @unittest.skip
    def test_fetch_all_comment(self):
        comment = {'text': 'testtesttest1', 'complaint_id': 1}
        response = self.app.post(
            CREATE_COMMENT_URL,
            data=json.dumps(comment),
            content_type='application/json',
        )
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'state': 'Success'})

        comment = {'text': 'testtesttest2', 'complaint_id': 1}
        response = self.app.post(
            CREATE_COMMENT_URL,
            data=json.dumps(comment),
            content_type='application/json',
        )
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'state': 'Success'})

        ##########################
        # Test fetch all comments
        ##########################
        response = self.app.get(
            FETCH_ALL_COMMENT_URL + '1', content_type='application/json'
        )
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data) > 1, True)

        # Delete all inserted comments.
        # response = self.app.delete(MVC_COMMENT_URL + '1')
        # self.assertEqual(response.status_code, 204)
        #
        # response = self.app.delete(MVC_COMMENT_URL + '2')
        # self.assertEqual(response.status_code, 204)
