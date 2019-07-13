from datetime import datetime

from marshmallow import fields
from marshmallow_sqlalchemy import TableSchema

from app import api
from app import db
from app.models import UserSchema


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), index=True)
    text = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class CommentResponse(TableSchema):
    class Meta:
        table = Comment.__table__
        exclude = ('id',)
        many = True

    complaint_id = fields.String(attribute='complaint_id')
    user = fields.Nested('UserSchema', many=False)


class CommentsResponse(TableSchema):
    CommentsResponse = fields.List(fields.Nested(CommentResponse), required=True)


comment_schema = CommentResponse()
comments_schema = CommentsResponse()

# TODO: only select a subtset of fields not all.
user_schema = UserSchema()


def comment_to_json(comment):
    user = comment.User
    dump_user_data = user_schema.dump(user).data
    dump_data = comment_schema.dump(comment).data
    dump_data['user'] = dump_user_data
    return dump_data


class CommentDAO(object):
    def __init__(self):
        self.OK = 'OK'

    def get(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            dump_data = comment_to_json(comment)
            return dump_data

        api.abort(404, "Comment by id {} doesn't exist".format(comment_id))

    def delete(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return 'deleted'
        else:
            api.abort(404, "Comment by id {} doesn't exist".format(comment_id))

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
            return comment_to_json(comment)
        else:
            api.abort(404, "Comment by id {} doesn't exist".format(comment_id))

    def fetch_all_by_complaintID(self, complaint_id):
        comments = Comment.query.filter(Comment.complaint_id == complaint_id).all()
        if comments:
            ret = []
            for comment in comments:
                dump_data = comment_to_json(comment)
                ret.append(dump_data)
            return ret
        else:
            return {}
