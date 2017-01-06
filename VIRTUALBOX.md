# VirtualBox setup

* Ubuntu ISO: `https://www.ubuntu.com/download/desktop`
* Update packages: `sudo apt-get update`

## Get the repo

* Install git: `sudo apt install git`
* Create a new SSH key and add it in GitHub: `ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
* Clone the repo: `git clone git@github.com:csakoda/hettyversion.git`

## Docker

* Add GPG key: `sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D`
* Add repo: `sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'`
* Update packages: `sudo apt-get update`
* Install from docker repo: `apt-cache policy docker-engine`
* Install docker: `sudo apt-get install -y docker-engine`
* Add user to group: `sudo usermod -aG docker $(whoami)`
* Install docker-compose: `sudo curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.8.1/docker-compose-$(uname -s)-$(uname -m)"`
* Set permissions for docker-compose: `sudo chmod +x /usr/local/bin/docker-compose`

## Python

* Upgrade pip: `pip install --upgrade pip`
* Install python3-venv: `sudo apt-get install python3-venv`
* Create a python3-venv: `python3 -m venv venv`
* Activate the venv: `source venv/bin/activate`
* Install mysqlclient deps: `sudo apt-get install python-dev python3-dev'
* `sudo apt-get install libmysqlclient-dev`
* `pip install pymysql`

## Launch

* `docker-compose up -d`
* `pip install -r requirements.txt`
* `python manage.py db upgrade`
* `python manage.py load_songdata`
* `python manage.py runserver`
