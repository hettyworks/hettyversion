import manage
import importlib
import hettyversion.versions
from hettyversion.database import db
from hettyversion.versions import fight_versions, init_rating, get_version, load_rating, get_candidate
from hettyversion.models import Song, Version

def reload():
    importlib.reload(hettyversion.versions)
