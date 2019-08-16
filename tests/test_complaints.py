import json

import pytest

from app.resources.complaints.models import Complaint


@pytest.mark.parametrize(
    ('by_type', 'query'),
    (
        ('byUser', 'phone_num=13312341234'),
        ('byMerchant', 'merchant_id=1'),
        ('byType', 'complaint_type=warranty'),
        ('last', 'n=5'),
    ),
)
def test_fetch_complaints(client, auth, by_type, query):
    auth.login()
    response = client.get('/api/complaints/{}?{}'.format(by_type, query))
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 1


def test_fetch_all_complaints(client, auth):
    auth.login('13344445555', 'Abcd3333')
    response = client.get('/api/complaints/all')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 1


def test_add_complaint(client, auth):
    auth.login()
    response = client.post(
        '/api/complaints',
        json={
            'merchant_id': 1,
            'complaint_body': 'eeeeeeees complain1',
            'expected_solution_body': '',
            'complain_type': 'product_issue',
            'if_negotiated_by_merchant': True,
            'negotiate_timestamp': '2019-06-07T19:12:44.468Z',
            'allow_public': True,
            'allow_contact_by_merchant': True,
            'allow_press': True,
            'item_price': '',
            'item_model': '',
            'trade_info': '',
            'relatedProducts': '',
            'purchase_timestamp': '2019-06-07T19:12:44.468Z',
            'invoice_files': [],
            'evidence_files': ['https://image-url.example.com'],
        },
    )
    assert response.status_code == 200

    data = Complaint.query.filter_by(user_id=1).all()
    assert len(data) == 2
