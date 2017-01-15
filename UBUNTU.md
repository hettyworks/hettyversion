# Ubuntu 16.04 setup from scratch

* Update packages: `sudo apt-get update`
* Install git: `sudo apt install git`
* Install python3-venv: `sudo apt-get install python3-venv`
* Install libmysqlclient-dev: `sudo apt-get install libmysqlclient-dev`
* Install python3-dev: `sudo apt-get install python3-dev`

* Create a new ssh key: `ssh-keygen -t rsa -b 4096 -C "example@gmail.com"` and add to GitHub
* Clone repository: `git clone git@github.com:hettyworks/hettyversion.git` and cd to hettyworks/

* Create new virtual environment: `python3 -m venv venv`
* Activate venv: `source venv/bin/activate`
* Install project dependencies: `pip install -r requirements.txt`

## Install latest Docker

* Install dependencies: `sudo apt-get install apt-transport-https ca-certificates`
* Add GPG key: `sudo apt-key adv \
               --keyserver hkp://ha.pool.sks-keyservers.net:80 \
               --recv-keys 58118E89F3A912897C070ADBF76221572C52609D`
* Add repository: `echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list`
* Update packages: `sudo apt-get update`
* Verify repository (optional): `apt-cache policy docker-engine`
* Install kernel packages: `sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual`
* Install docker: `sudo apt-get install docker-engine`
* Start daemon: `sudo service docker start`
* Test install: `sudo docker run hello-world`
* Update user permissions: `sudo usermod -aG docker $USER`
* Log out and back in
* Test install without sudo: `docker run hello-world`
