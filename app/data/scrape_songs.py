from bs4 import BeautifulSoup
import urllib.request

opener = urllib.request.FancyURLopener({})
url = "http://phish.net/songs"
f = opener.open(url)
soup = BeautifulSoup(f)

songs = soup.find_all('tr')[1:]

def go():
    names = list(set([s.td.a.text.encode('utf-8') for s in songs]))
    names.sort()
    for name in names:
        print(name)
