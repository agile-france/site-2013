#!/usr/bin/env bash

apt-get update
sudo apt-get -y install make python-pip
sudo locale-gen --no-purge --lang 'fr_FR'
sudo pip install s3vcp markdown pelican==3.2 --use-mirrors
