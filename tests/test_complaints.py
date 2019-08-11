import json

from app.resources.complaints.models import Complaint


def test_fetch_all_complaint(client, auth):
    auth.login()
    response = client.get('/complaints/byUser?phone_num=13312341234')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 1


def test_add_complaint(client, auth):
    auth.login()
    response = client.post(
        '/complaints',
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
