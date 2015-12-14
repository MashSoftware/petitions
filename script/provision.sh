#!/usr/bin/env bash

echo 'Updating package lists...'
apt-get -qq  update

echo 'Upgrading packages...'
apt-get -qq -y upgrade

echo 'Installing Pip...'
apt-get -qq -y install python-pip

echo 'Installing requirements...'
pip install -r /vagrant/requirements.txt

echo 'Tidying up...'
apt-get -qq autoclean
apt-get -qq autoremove

echo 'Done!'
echo 'You must set your "They Work For You API Key": export TWFY_API_KEY=<API_KEY>'
