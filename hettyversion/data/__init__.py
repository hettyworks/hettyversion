from sqlalchemy.sql import select
from bs4 import BeautifulSoup
import urllib.request
from hettyversion.models import Song
from hettyversion.database import db

def get_band_id(name):
    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'band':
            s = select([table]).where(table.c.name == name)
            result = db.session.execute(s)
    return result.fetchone().band_id    


def get_song_id(name):
    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'song':
            s = select([table]).where(table.c.name == name)
            result = db.session.execute(s)
    return result.fetchone().song_id


def get_version_by_id(id):
    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'version':
            s = select([table]).where(table.c.version_id == id)
            result = db.session.execute(s)
    return result.fetchone()

def get_song_by_id(id):
    meta = db.metadata
    for table in meta.sorted_tables:
        if table.name == 'song':
            s = select([table]).where(table.c.song_id == id)
            result = db.session.execute(s)
    return result.fetchone()

def get_song_by_phishin_id(id):
    return db.session.query(Song).filter(Song.phishin_id == id).one()


def get_song_versions(name):
    error_count = 0
    opener = urllib.request.FancyURLopener({})
    url = "http://phish.net/songs/" + name.replace(' ', '-').lower()

    f = opener.open(url)
    soup = BeautifulSoup(f, 'html.parser')
    versions = soup.find_all('tr')[1:]
    dates = list()
    for s in versions:
        try:
            dates.append(s.td.a.text)
        except AttributeError:
            print('Skipping bad version.')
            error_count += 1
            pass
    dates.sort()
    print('{0} bad version{1} skipped.'.format(error_count, 's' if error_count > 1 else ''))
    return dates
