from app.database import db

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    version_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    created_by = db.Column(db.Integer)
    created = db.Column(db.DateTime)
