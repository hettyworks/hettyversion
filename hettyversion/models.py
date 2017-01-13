from hettyversion.database import db
from flask_user import UserMixin


class Band(db.Model):
    band_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.Text)


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    version_id = db.Column(db.Integer)
    content = db.Column(db.Text)
    created_by = db.Column(db.Integer)
    created = db.Column(db.DateTime)


class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.String(128))
    band_id = db.Column(db.Integer, db.ForeignKey("band.band_id"), index=True)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')


class Version(db.Model):
    version_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    date = db.Column(db.Date)
    created = db.Column(db.DateTime)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"))
    url = db.Column(db.String(256))
    created_by = db.Column(db.Integer)
    mu = db.Column(db.Float)
    sigma = db.Column(db.Float)


class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    lhs = db.Column(db.Integer)
    rhs = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    created_by = db.Column(db.Integer)
    created = db.Column(db.DateTime)
