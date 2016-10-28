#!/usr/bin/env bash

echo 'Setting locale...'
sudo locale-gen en_GB.UTF-8

echo 'Upgrading packages...'
sudo apt-get update
sudo apt-get -y upgrade

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
