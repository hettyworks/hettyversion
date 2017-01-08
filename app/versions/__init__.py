from enum import Enum
from app.database import db
from app.versions.model import Version
import app.versions.views
from trueskill import Rating, rate_1vs1

class Winner(Enum):
    LEFT = 1
    RIGHT = 2

def fight(lhs, rhs, winner):
    if winner == Winner.LEFT:
        lhs, rhs = rate_1vs1(lhs, rhs)
    elif winner == Winner.RIGHT:
        rhs, lhs = rate_1vs1(rhs, lhs)
    return lhs, rhs

def load_version(version_id):
    v = db.session.query(Version).\
          filter(Version.version_id == version_id)[0]
    return Rating(v.mu, v.sigma)

def set_rating(version_id):
    v = db.session.query(Version).\
          filter(Version.version_id == version_id)[0]
    r = Rating()
    v.mu = r.mu
    v.sigma = r.sigma
    db.session.commit()
