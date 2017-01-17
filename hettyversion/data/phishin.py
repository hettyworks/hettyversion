from sqlalchemy.schema import MetaData, DropConstraint
from bs4 import BeautifulSoup
import urllib.request
import json
from pprint import PrettyPrinter

from hettyversion.database import db
from hettyversion.models import Band, Song


pp = PrettyPrinter(indent=4)


def phishin_load_all():
    clear_db()
    band_id = create_phish()
    load_all_songs(band_id)


def create_phish():
    b = Band()
    b.name = 'Phish'
    db.session.add(b)
    db.session.commit()
    db.session.refresh(b)
    return b.band_id


def load_all_songs(band_id):
    songs = get_all_songs()

    for song in songs:
        s = Song()
        s.name = song['title']
        # s.phishin_id
        s.band_id = band_id
        db.session.add(s)
    db.session.commit()


def get_all_songs():
    print('Scraping all songs...')
    songs_master = []

    i = 43
    while i < 99:  # sanity check
        opener = urllib.request.FancyURLopener({})
        url = "http://phish.in/api/v1/songs?page={}".format(str(i))
        f = opener.open(url)
        soup_songs = BeautifulSoup(f, 'html.parser')
        json_songs = json.loads(str(soup_songs))
        if not json_songs['data']:
            break

        songs_master = songs_master + json_songs['data']
        i += 1

    print('Done.')
    return songs_master


def clear_db():
    print('Clearing db...')
    metadata = MetaData(db.engine)
    metadata.reflect()
    for table in metadata.tables.values():
        for fk in table.foreign_keys:
            db.engine.execute(DropConstraint(fk.constraint))
    
    meta = db.metadata
    for table in meta.sorted_tables:
            print('Clear table: {}'.format(table.name))
            db.session.execute(table.delete())
    db.session.commit()
    print ('Done.')