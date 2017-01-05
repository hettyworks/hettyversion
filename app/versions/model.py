from app.database import db

class Version(db.Model):
    version_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    date = db.Column(db.Date)
    created = db.Column(db.DateTime)
    song_id = db.Column(db.Integer)
    url = db.Column(db.String(256))
    created_by = db.Column(db.Integer)
