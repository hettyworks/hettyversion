from app.database import db

class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    lhs = db.Column(db.Integer)
    rhs = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    created_by = db.Column(db.Integer)
    created = db.Column(db.DateTime)
