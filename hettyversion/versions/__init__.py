from sqlalchemy import and_, or_
from enum import Enum
from hettyversion.database import db
from hettyversion.models import Version, Song, Vote
from trueskill import Rating, rate_1vs1
from flask_user import current_user, login_required


class Winner(Enum):
    LEFT = 1
    RIGHT = 2

def fight_versions(lhs_id, rhs_id, id_winner):
    if lhs_id == id_winner:
        winner = Winner.LEFT
    else:
        winner = Winner.RIGHT
    lhs, rhs = fight(load_rating(lhs_id), load_rating(rhs_id), winner)
    update_rating(lhs_id, lhs)
    update_rating(rhs_id, rhs)

def get_version(version_id):
    return db.session.query(Version).\
        filter(Version.version_id == version_id)[0]

def update_rating(version_id, rating):
    v = get_version(version_id)
    v.mu = rating.mu
    v.sigma = rating.sigma
    db.session.commit()

def fight(lhs, rhs, winner):
    if winner == Winner.LEFT:
        lhs, rhs = rate_1vs1(lhs, rhs)
    elif winner == Winner.RIGHT:
        rhs, lhs = rate_1vs1(rhs, lhs)
    return lhs, rhs

def load_rating(version_id):
    v = get_version(version_id)
    if not v.mu:
        v = init_rating(v)
    return Rating(v.mu, v.sigma)

def init_rating(v):
    r = Rating()
    v.mu = r.mu
    v.sigma = r.sigma
    db.session.commit()
    return v

def get_candidate(band_id=1):
    # for current_user.id
    # lookup songs that have at least 2 versions, choose one
    # choose a version, iterate through the rest of the versions,
    # looking for a pair that current_user.id has not already rated
    # present the first found
    # this logic is dumb as can be at present (poor performance)
    user_id = current_user.id if current_user else 0
    for song_id, in db.session.query(Song.song_id).filter(Song.band_id == 1).all():
        versions = db.session.query(Version).filter(Version.song_id == song_id).all()
        if versions:
            print(versions)
        for lhs in versions:
            for rhs in versions:
                if lhs != rhs:
                    if db.session.query(Vote).\
                       filter(and_(Vote.created_by == user_id,
                                   or_(and_(Vote.lhs == lhs.version_id,
                                            Vote.rhs == rhs.version_id),
                                       and_(Vote.lhs == rhs.version_id,
                                            Vote.rhs == lhs.version_id)))).count() == 0:
                        # user hasn't voted
                        return lhs, rhs
    raise Exception("Couldn't find a pair for user")
