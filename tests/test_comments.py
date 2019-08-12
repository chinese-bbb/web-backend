import json

from app.resources.comments.models import Comment


def test_fetch_all_comment_of_complaint(client, auth):
    auth.login()
    response = client.get('/api/comments/byComplaint/1')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 3


def test_add_comment(client, auth):
    auth.login()
    response = client.post('/api/comments', json={'text': 'abcd', 'complaint_id': 1})
    assert response.status_code == 200

    data = Comment.query.filter_by(complaint_id=1, user_id=1).all()
    assert len(data) == 4
