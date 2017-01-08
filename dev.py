import manage
import importlib
import hettyversion.versions
from hettyversion.versions import fight_versions, init_rating, get_version, load_rating

def reload():
    importlib.reload(hettyversion.versions)
