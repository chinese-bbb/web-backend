from datetime import datetime

from app.extensions import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    text = db.Column(db.Text())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), index=True)
