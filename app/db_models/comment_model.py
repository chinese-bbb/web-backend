from datetime import datetime
from app import application, db, api
from marshmallow_sqlalchemy import ModelSchema, fields_for_model, TableSchema

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), index=True)
    text = db.Column(db.String(5000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class CommentSchema(TableSchema):
    class Meta:
        table = Comment.__table__
        include_fk = True
        exclude = ("id",)
        many= True
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

    def update(self, comment_id, text):
        comment = Comment.query.filter_by(id=comment_id).first()
        if comment:
            Comment.query.filter_by(id = comment_id).update({'text': text})
            db.session.commit()

            comment = Comment.query.filter_by(id=comment_id).first()
            return comment_schema.dump(comment).data
        else:
            api.abort(404, "Comment by id {} doesn't exist".format(comment_id))


    def fetch_all_by_complaintID(self, complaint_id):
        comments = Comment.query.filter(Comment.complaint_id == complaint_id).all()
        if comments:
            ret = []
            for comment in comments:
                dump_data = comment_schema.dump(comment).data
                ret.append(dump_data)
            return ret
        else:
            api.abort(404, "complaint_id by id {} doesn't exist in comment table".format(complaint_id))
