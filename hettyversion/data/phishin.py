from sqlalchemy.schema import MetaData, DropConstraint
from bs4 import BeautifulSoup
import urllib.request
import json
from pprint import PrettyPrinter

from hettyversion.database import db
from hettyversion.models import Band, Song, Version


pp = PrettyPrinter(indent=4)


class PhishinLoader:
    def __init__(self):
        pass


    def load_all(self):
        self.clear_db()
        self.create_phish()
        self.load_all_songs()
        self.load_all_versions()


    def create_phish(self):
        b = Band()
        b.name = 'Phish'
        db.session.add(b)
        db.session.commit()
        db.session.refresh(b)
        self.band_id = b.band_id


    def load_all_songs(self):
        songs = self.get_all_songs()

        for song in songs:
            s = Song()
            s.name = song['title']
            s.band_id = self.band_id
            s.phishin_id = song['id']
            db.session.add(s)
        db.session.commit()
        print('Songs loaded.')


    def load_all_versions(self):
        versions = self.get_all_versions()

        # for version in versions:
        #     v = Version()
        #     v.title = 
        print('Versions loaded.')


    def get_all_versions(self):
        versions_master = []

        i = 1400
        while i < 1401:  # sanity check
            opener = urllib.request.FancyURLopener({})
            url = "http://phish.in/api/v1/tracks?page={}".format(str(i))
            f = opener.open(url)
            soup_versions = BeautifulSoup(f, 'html.parser')
            json_versions = json.loads(str(soup_versions))
            if not json_versions['data']:
                break

            versions_master = versions_master + json_versions['data']
            i += 1
        pp.pprint(versions_master)
        print('Versions scraped.')
        return versions_master


    def get_all_songs(self):
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
        print('Songs scraped.')
        return songs_master


    def clear_db(self):
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
        print('DB cleared.')