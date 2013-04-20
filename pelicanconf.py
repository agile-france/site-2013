#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2.ext import loopcontrols
from pelican.utils import slugify

from os.path import dirname
import sys

sys.path.insert(0, dirname(__file__))

from plugins import conference

AUTHOR = u"L'équipe d'organisation"
SITENAME = u'Agile France 2013'
SITEURL = ''
TWITTER_USERNAME = "AgileFrance"
TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'fr'

MENUITEMS = [
	(u'Inscription', '/index.html'),
	(u'Appel à Orateurs', '/orateur.html'),
	(u'Programme', '/static/programme/programme-agile-france-2013-draft-2.pdf'),
	(u'Sessions', lambda sessions: [(s.title, '/' + s.url) for s in sessions]),
	(u'Blog', '/archives.html'),
	(u'Éditions précédentes', [
		(u'2006 - restauration en cours', '#'),
		(u'2007 - restauration en cours', '#'),
		(u'2008', 'http://2009.conference-agile.fr/conf.agile-france.org/2008_programme.html'),
		(u'2009', 'http://2009.conference-agile.fr'),
		(u'2010 - restauration en cours', '#'),
		(u'2011 - restauration en cours', '#'),
		(u'2012', 'http://2012.conference-agile.fr'),
		],)
	]

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'


GOOGLE_ANALYTICS = 'UA-36421002-1'

DEFAULT_PAGINATION = 10

THEME = 'themes/ericka'

# Color Stylesheet - orange, blue, pink, brown, red or green
CSS_FILE = 'orange.css'

INDEX_SAVE_AS = False

JINJA_EXTENSIONS = [loopcontrols]

TEMPLATE_PAGES = {'js/custom.js': 'theme/js/custom.js'}

PLUGINS = [conference]

ARTICLE_EXCLUDES = ['pages', 'speakers', 'sessions']

SESSION_DIR = 'sessions'
SESSION_EXCLUDES = ''
SESSION_SAVE_AS = 'sessions/{slug}.html'
SESSION_URL = 'sessions/{slug}.html'

SPEAKER_DIR = 'speakers'
SPEAKER_EXCLUDES = ''
SPEAKER_SAVE_AS = 'speakers/{slug}.html'
SPEAKER_URL = 'speakers/{slug}.html'


def apostrophe(article, nom):
	if nom[0].lower() in "aeiouy":
		return article[:-1] + "'" + nom
	else:
		return article + ' ' + nom

JINJA_FILTERS = {'apostrophe': apostrophe, 'slugify': slugify}

STATIC_PATHS = ['programme']
