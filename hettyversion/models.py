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
    band_id = db.Column(db.Integer, index=True)
    phishin_id = db.Column(db.Integer)


class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key=True)
    phishin_id = db.Column(db.Integer)
    location = db.Column(db.String(128))
    name = db.Column(db.String(128))


class Show(db.Model):
    show_id = db.Column(db.Integer, primary_key=True)
    phishin_id = db.Column(db.Integer)
    venue_id = db.Column(db.Integer)
    date = db.Column(db.String(128))

class Version(db.Model):
    version_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    created = db.Column(db.DateTime)
    song_id = db.Column(db.Integer) # Song.phishin_id
    url = db.Column(db.String(256))
    created_by = db.Column(db.Integer)
    mu = db.Column(db.Float)
    sigma = db.Column(db.Float)
    phishin_id = db.Column(db.Integer)
    show_id = db.Column(db.Integer)


class ListenedTo(db.Model):
    lt_id = db.Column(db.Integer, primary_key=True)
    version_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))

# Define Role model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define UserRoles model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class VersionComment(db.Model):
    versioncomment_id = db.Column(db.Integer, primary_key=True)
    version_id = db.Column(db.Integer, db.ForeignKey('version.version_id', ondelete='NO ACTION'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='NO ACTION'))
    body = db.Column(db.Text)
    comment_date = db.Column(db.DateTime())


class VersionCommentVote(db.Model):
    versioncommentvote_id = db.Column(db.Integer, primary_key=True)
    version_id = db.Column(db.Integer, db.ForeignKey('version.version_id', ondelete='NO ACTION'))
    voter_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='NO ACTION'))
    value = db.Column(db.Integer)
    vote_date = db.Column(db.DateTime())


class Vote(db.Model):
    vote_id = db.Column(db.Integer, primary_key=True)
    lhs = db.Column(db.Integer)
    rhs = db.Column(db.Integer)
    winner = db.Column(db.Integer)
    created_by = db.Column(db.Integer)
    created = db.Column(db.DateTime)
