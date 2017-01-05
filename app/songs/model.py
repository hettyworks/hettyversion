from app.database import db

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.String(128))
    bandid = db.Column(db.Integer)
