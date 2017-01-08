from enum import Enum
from hettyversion.database import db
from hettyversion.models import Version
from trueskill import Rating, rate_1vs1

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
