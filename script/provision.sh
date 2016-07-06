#!/usr/bin/env bash

echo 'Installing PostgreSQL & PostGIS...'
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
sudo apt-get install wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y postgresql-9.5-postgis-2.2 pgadmin3 postgresql-contrib postgis libpq-dev python-dev
sudo locale-gen en_GB.UTF-8

echo 'Installing Pip...'
apt-get -y install python-pip

echo 'Upgrade Pip...'
pip install -U pip

echo 'Installing requirements...'
pip install -r /vagrant/requirements.txt

echo 'Tidying up...'
apt-get autoclean
apt-get autoremove

echo 'Done!'
