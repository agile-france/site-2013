#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2.ext import loopcontrols

AUTHOR = u"L'équipe d'organisation"
SITENAME = u'Agile France 2013'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'fr'

# Blogroll
LINKS =  (('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
          ('Python.org', 'http://python.org'),
          ('Jinja2', 'http://jinja.pocoo.org'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

THEME = 'themes/ericka'

INDEX_SAVE_AS = False

JINJA_EXTENSIONS = [loopcontrols]
