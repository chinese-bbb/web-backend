from flask import abort

from .models import Comment
from app.extensions import db


class CommentDAO(object):
    def __init__(self):
        self.OK = 'OK'

    def get(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            return comment

        abort(404, "Comment by id {} doesn't exist".format(comment_id))

    def delete(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return 'deleted'
        else:
            abort(404, "Comment by id {} doesn't exist".format(comment_id))

    def create(self, data):
        comment = Comment(**data)
        db.session.add(comment)
        db.session.commit()
        return 'OK'

    def update(self, comment_id, text):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            Comment.query.filter_by(id=comment_id).update({'text': text})
            db.session.commit()

            comment = Comment.query.filter_by(id=comment_id).first()
            return comment
        else:
            abort(404, "Comment by id {} doesn't exist".format(comment_id))

    def fetch_all_by_complaintID(self, complaint_id):
        comments = Comment.query.filter(Comment.complaint_id == complaint_id).all()
        if comments:
            return comments
        else:
            return []
