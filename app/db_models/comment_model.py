from datetime import datetime
from app import application, db, api
from marshmallow_sqlalchemy import ModelSchema, fields_for_model, TableSchema

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    text = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class CommentSchema(TableSchema):
    class Meta:
        table = Comment.__table__
        include_fk = True
        exclude = ("id",)
    # complaint_id = fields.String(attribute="id")

comment_schema = CommentSchema()

class CommentDAO(object):
    def __init__(self):
        self.OK = "OK"

    def get(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            dump_data = comment_schema.dump(comment).data
            print(dump_data)
            return dump_data

        api.abort(404, "Comment by id {} doesn't exist".format(comment_id))

    def delete(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return "deleted"
        else:
            api.abort(404, "Comment by id {} doesn't exist".format(comment_id))


    def create(self, data):
        comment = Comment(**data)
        db.session.add(comment)
        db.session.commit()
        return "OK"

    def fetchByUserId(self, phone_num):
        api.abort(404, "Complaint by user {} doesn't exist".format(phone_num))

