import manage
import importlib
import app.versions
from app.versions import fight_versions, init_rating, get_version, load_rating

def reload():
    importlib.reload(app.versions)
