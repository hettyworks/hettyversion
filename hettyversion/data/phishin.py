from sqlalchemy.schema import MetaData, DropConstraint
from bs4 import BeautifulSoup
import urllib.request
import json
from pprint import PrettyPrinter

from hettyversion.database import db
from hettyversion.models import Band, Song, Version


pp = PrettyPrinter(indent=4)


class PhishinLoader:
    songs = []
    versions = []
    shows = []
    venues = []


    def __init__(self):
        pass


    def load_all(self):
        self.songs = self.get_all_songs()
        self.versions = self.get_all_versions()
        self.shows = self.get_all_shows()
        self.venues = self.get_all_venues()
        self.data_to_json()


    def data_to_json(self):
        master_dict = {}
        master_dict['songs'] = self.songs
        master_dict['versions'] = self.versions
        master_dict['shows'] = self.shows
        master_dict['venues'] = self.venues

        with open('phishin.json', 'w+') as outfile:
            json.dump(master_dict, outfile, indent=2)


    def create_phish(self):
        b = Band()
        b.name = 'Phish'
        db.session.add(b)
        db.session.commit()
        db.session.refresh(b)
        self.band_id = b.band_id


    def get_all_venues(self):
        venues_master = []

        i = 33
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
        pp.pprint(venues_master)
        print('Venues scraped.')
        return venues_master


    def get_all_shows(self):
        shows_master = []

        i = 76
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
        pp.pprint(shows_master)
        print('Shows scraped.')
        return shows_master


    def get_all_versions(self):  # has to be line by line
        versions_master = []

        i = 1400
        while i < 1401:  # sanity check
            opener = urllib.request.FancyURLopener({})
            url = "http://phish.in/api/v1/tracks?page={}".format(str(i))
            f = opener.open(url)
            soup = BeautifulSoup(f, 'html.parser')
            soup_list = json.loads(str(soup))
            if not soup_list['data']:
                break

            versions_master = versions_master + soup_list['data']
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
            soup = BeautifulSoup(f, 'html.parser')
            soup_list = json.loads(str(soup))
            if not soup_list['data']:
                break

            songs_master = songs_master + soup_list['data']
            i += 1
        print('Songs scraped.')
        return songs_master
