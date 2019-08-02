import json

from tests.test_base import BaseTestClass

TEST_BASE_URL = 'http://0.0.0.0:5000/'
DOC_URL = '{}/doc/'.format(TEST_BASE_URL)
LOGIN_URL = '{}/api/login'.format(TEST_BASE_URL)


class Test_basic_API(BaseTestClass):
    def setUp(self):
        super().setUp()

    def test_get_doc_page(self):
        response = self.app.get(DOC_URL)
        print(response)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        user = {'phone_num': '13333333333', 'password': 'Abcd3333'}
        response = self.app.post(
            LOGIN_URL, data=json.dumps(user), content_type='application/json'
        )
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, 'OK')
