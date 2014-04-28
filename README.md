site-2013
=========

Le source pour le site de la conf 2013.
Le déploiement est assuré par travis. [![Build Status](https://travis-ci.org/agile-france/site-2013.png?branch=master)](https://travis-ci.org/agile-france/site-2013)

Installation du site en local :
===============================

Vous aurez besoin de
- git
- python
- pip
- pelican
- Markdown

Quelques commandes (je laisse les personnes n'ayant pas github d'installé sur leur machine, ou fonctionnant sous windows completer si nécéssaire)  
git clone https://github.com/agile-france/site-2013.git
sudo apt-get install python-pip  
sudo pip install pelican==3.2  
sudo pip install Markdown  
make clean  
make html  
make serve
