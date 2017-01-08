# hettyversion

## Basic Setup

```
docker-compose up -d
pip3.4 install -r requirements.txt
python3.4 manage.py db upgrade
python3.4 manage.py load_songdata
python3.4 manage.py runserver
```

### Flask-Mail note (required)

You must create an email app password and store that and your gmail address in MAIL_PASSWORD and MAIL_USERNAME, respectively: `https://security.google.com/settings/security/apppasswords`

Flask-Admin is available here

* <http://localhost:5000/admin/>

## Windows PowerShell dev setup (incomplete)

### Install Docker

### Install Windows dependencies (not sure exactly which combination is sufficient):

* Download & install Visual Studio 2015: `https://www.visualstudio.com/downloads/`
* Download & install .NET Framework 4: `https://www.microsoft.com/en-us/download/details.aspx?id=17851`
* Download & install the Microsoft Windows SDK: `http://www.microsoft.com/en-us/download/details.aspx?id=8279`

### Install Python

* Install Python3.4
* Install virtualenv
* Create virtualenv & activate: `virtualenv -p C:\Python34\python.exe venv`
* Install python deps: `pip install -r requirements.txt`

## Design

### Core Features

* A headyversion.com clone with support for arbitrary song lists and multiple bands
* A head-to-head version ranking game (e.g. http://www.allourideas.org/)
* Generate ELO & ranking of any given version

### Tech Stack

* Python 3.4
* Flask
* Docker

### Schema Design

- [ ] users: ID, username, hashpw, role, registered_timestamp
- [x] songs: ID, name, desc, bandid
- [x] versions: ID, title, datestamp_source, timestamp_added, songid, link (optional), added_by
- [x] bands: ID, name, desc
- [x] votes: ID, userid, version1id, version2id, winnerid, timestamp
- [x] comments: ID, userid, content, versionid, timestamp

### Pages

* login, logout, register, resetpw
* home page, list of bands, list of all songs, single band page w/list of their songs, single song page w/list of versions, single version page, h2h between versions page
* add version, edit version, delete version (admin)
* add song (admin), edit song (admin), delete song (admin)
* add band (admin), edit band (admin), delete band (admin)

### Questions

* How will we manage scores? 
  * http://trueskill.org/

### Future

* Verification of versions
* Verification of new bands
* Verification of new songs

## VirtualBox setup

* Ubuntu ISO: `https://www.ubuntu.com/download/desktop`
* Update packages: `sudo apt-get update`

### Get the repo

* Install git: `sudo apt install git`
* Create a new SSH key and add it in GitHub: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
* Clone the repo: `git clone git@github.com:csakoda/hettyversion.git`

### Docker

* Add GPG key: `sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D`
* Add repo: `sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'`
* Update packages: `sudo apt-get update`
* Install from docker repo: `apt-cache policy docker-engine`
* Install docker: `sudo apt-get install -y docker-engine`
* Add user to group: `sudo usermod -aG docker $(whoami)`
* Install docker-compose: `sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.8.1/docker-compose-$(uname -s)-$(uname -m)"`
* Set permissions for docker-compose: `sudo chmod +x /usr/local/bin/docker-compose`

### Python

* Upgrade pip: `pip install --upgrade pip`
* Install python3-venv: `sudo apt-get install python3-venv`
* Create a python3-venv: `python3 -m venv venv`
* Activate the venv: `source venv/bin/activate`
* Install mysqlclient deps: `sudo apt-get install python-dev python3-dev'
* `sudo apt-get install libmysqlclient-dev`
* `pip install pymysql`

### Launch

* `docker-compose up -d`
* `pip install -r requirements.txt`
* `python manage.py db upgrade`
* `python manage.py load_songdata`
* `python manage.py runserver`