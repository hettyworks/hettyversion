from bs4 import BeautifulSoup
import urllib.request

def get_song_names():
    opener = urllib.request.FancyURLopener({})
    url = "http://phish.net/songs"
    f = opener.open(url)
    soup = BeautifulSoup(f)

    songs = soup.find_all('tr')[1:]

    names = list(set([s.td.a.text.encode('utf-8') for s in songs]))
    names.sort()
    return names
