from sqlalchemy.schema import MetaData, DropConstraint
from bs4 import BeautifulSoup
import urllib.request
import json
from pprint import PrettyPrinter
import time

from hettyversion.database import db
from hettyversion.models import Band, Song, Version, Venue


pp = PrettyPrinter(indent=4)


def load_from_json(app):
    target = app.root_path + '/data/phishin.json'
    with open(target) as infile:
        data = json.load(infile)

    # clear_db()
    # band_id = create_phish()
    band_id = 1
    load_venues(data['venues'])
    load_shows(data['shows'])
    load_songs(data['songs'], band_id)
    load_versions(data['versions'])


def create_phish():
    b = Band()
    b.name = 'Phish'
    db.session.add(b)
    db.session.commit()
    db.session.refresh(b)
    return b.band_id


def load_venues(venues):
    for venue in venues:
        v = Venue()
        v.name = venue['name']
        v.location = venue['location']
        v.phishin_id = venue['id']
        db.session.add(s)
    db.session.commit()


def load_shows(shows):
    for show in shows:
        s = Show()
        s.phishin_id = shows['id']
        s.venue_id = shows['venue_id']
        s.date = shows['date']
        db.session.add(s)
    db.session.commit()


def load_songs(songs, band_id):
    for song in songs:
        s = Song()
        s.band_id = band_id
        s.phishin_id = song['id']
        # s.show_id = song['show_id']
        s.name = song['name']
        db.session.add(s)
    db.session.commit()


def load_versions(versions):
    for version in versions:
        v = Version()
        v.date = version['show_date']
        v.song_id = version['song_ids'][0]  # might want to turn this into a join table to handle multiple song_ids
        v.url = version['mp3']
        v.phishin_id = version['id']
        v.show_id = version['show_id']


def clear_db():
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


class PhishinLoader:
    songs = []
    versions = []
    shows = []
    venues = []


    def __init__(self):
        pass


    def load_all(self):
        start = time.time()
        print('Scraping started.')
        self.songs = self.get_all_songs()
        print('{} songs scraped.'.format(len(self.songs)))
        self.shows = self.get_all_shows()
        print('{} shows scraped.'.format(len(self.shows)))
        self.venues = self.get_all_venues()
        print('{} venues scraped.'.format(len(self.venues)))
        self.versions = self.get_all_versions()
        print('{} versions scraped.'.format(len(self.versions)))
        self.data_to_json()
        end = time.time()
        print('Scraping completed in {0:.1f} seconds.'.format(end - start))


    def data_to_json(self):
        master_dict = {}
        master_dict['songs'] = self.songs
        master_dict['versions'] = self.versions
        master_dict['shows'] = self.shows
        master_dict['venues'] = self.venues

        with open('phishin.json', 'w+') as outfile:
            outfile.truncate()
            json.dump(master_dict, outfile)


    def get_all_venues(self):
        venues_master = []

        i = 1
        while i < 75:  # sanity check
            opener = urllib.request.FancyURLopener({})
            url = "http://phish.in/api/v1/venues?page={}".format(str(i))
            f = opener.open(url)
            soup = BeautifulSoup(f, 'html.parser')
            soup_list = json.loads(str(soup))
            if not soup_list['data']:
                break

            venues_master = venues_master + soup_list['data']
            i += 1
        return venues_master


    def get_all_shows(self):
        shows_master = []

        i = 1
        while i < 150:  # sanity check
            opener = urllib.request.FancyURLopener({})
            url = "http://phish.in/api/v1/shows?page={}".format(str(i))
            f = opener.open(url)
            soup = BeautifulSoup(f, 'html.parser')
            soup_list = json.loads(str(soup))
            if not soup_list['data']:
                break

            shows_master = shows_master + soup_list['data']
            i += 1
        return shows_master


    def get_all_songs(self):
        songs_master = []

        i = 1
        while i < 99:  # sanity check
            opener = urllib.request.FancyURLopener({})
            url = "http://phish.in/api/v1/songs?page={}".format(str(i))
            f = opener.open(url)
            soup = BeautifulSoup(f, 'html.parser')
            soup_list = json.loads(str(soup))
            if not soup_list['data']:
                break

            songs_master = songs_master + soup_list['data']
            i += 1
        return songs_master


    def get_all_versions(self):  # has to be line by line
        versions_temp = []

        i = 1
        while i < 2500:  # sanity check
            opener = urllib.request.FancyURLopener({})
            url = "http://phish.in/api/v1/tracks?page={}".format(str(i))
            f = opener.open(url)
            soup = BeautifulSoup(f, 'html.parser')
            soup_list = json.loads(str(soup))
            if not soup_list['data']:
                break

            versions_temp = versions_temp + soup_list['data']
            i += 1

        versions_master = self.get_all_versions_singly(versions_temp)

        return versions_master


    def get_all_versions_singly(self, versions_temp):
        versions_master = []

        for version in versions_temp:
            new_version = self.get_one_version(version['id'])
            if new_version: versions_master.append(new_version)
            # break

        return versions_master


    def get_one_version(self, version_id):
        opener = urllib.request.FancyURLopener({})
        url = "http://phish.in/api/v1/tracks/{}".format(version_id)
        f = opener.open(url)
        soup = BeautifulSoup(f, 'html.parser')
        soup_list = json.loads(str(soup))

        if not soup_list['data']:
            return False

        return soup_list['data']
