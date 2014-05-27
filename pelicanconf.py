#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2.ext import loopcontrols

from os.path import dirname
import sys
from pelican.utils import slugify
import logging

logger = logging.getLogger(__name__)

sys.path.insert(0, dirname(__file__))

from plugins import conference

AUTHOR = u"L'équipe d'organisation"
SITENAME = u'Conférence Agile France 2014'
SITEURL = ''
TWITTER_USERNAME = "AgileFrance"
TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'fr'

LOCALE = ['fr_FR.utf8', 'fra_fra']

def MENUITEMS(session_info):
	def session_list_menu(sessions):
		return [(s.title, '/' + s.url) for s in sessions]

	def sessions_by_tag(tags):
		categories = [u"Keynote", u"Produit", u"Collaborer", u"Construire", u"Organisation", u"Bouffée d'air frais"]
		return [(category, session_list_menu(tags[category])) for category in categories]

	return [
		(u'Accueil', '/index.html'),
		(u'Appel à Orateurs', '/pages/appel-a-orateurs.html'),
		(u'Programme', '/programme_2014.html'),
		(u'Sessions', [
			(u'Toutes', session_list_menu(session_info.sessions.all))] + sessions_by_tag(session_info.sessions.by_tag) ),
		(u'FAQ', '/pages/faq.html'),
		(u'Blog', '/archives.html'),
		(u'Informations', [
			(u'Accès', '/acces.html'),
			(u'Orateurs', '/pages/les-orateurs.html'),
			(u'Organisateurs', '/pages/lequipe-dorganisation.html')
		]),
		(u'Éditions précédentes', [
			(u'2013', 'http://2013.conference-agile.fr'),
			(u'2012', 'http://2012.conference-agile.fr'),
			(u'2011 - restauration en cours', '#'),
			(u'2010 - restauration en cours', '#'),
			(u'2009', 'http://2009.conference-agile.fr'),
			(u'2008', 'http://2009.conference-agile.fr/conf.agile-france.org/2008_programme.html'),
			(u'2007 - restauration en cours', '#'),
			(u'2006 - restauration en cours', '#'),
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

PLUGINS = [conference]

ARTICLE_EXCLUDES = ['pages', 'bios', 'sessions']

SESSION_DIR = 'sessions/current'
SESSION_EXCLUDES = ''
SESSION_SAVE_AS = 'sessions/{slug}.html'
SESSION_URL = 'sessions/{slug}.html'

BIO_DIR = 'bios/current'
BIO_EXCLUDES = ''
BIO_SAVE_AS = 'bios/{slug}.html'
BIO_URL = 'bios/{slug}.html'
BIO_PIC_PATH = 'trombines'

ROLE_NAMES = {
	'perfecter': {'M': u'Relecteur', 'F': u'Relectrice'},
	'organizer': {'M': u'Organisateur', 'F': u'Organisatrice'},
	'speaker': {'M': u'Orateur', 'F': u'Oratrice'},
	'aux': {'M': u'aux', 'F': u'aux'},
}

ROOM_NAMES = {
	'1': u'1 - Belvédère',
	'2': u'2 - Chalet RdC',
	'3': u'3 - Chalet 1er étage',
	'4': u'4 - Chalet 1er étage',
	'5': u'5 - Chalet 1er étage',
	'6': u'6 - Fermette',
}

def apostrophe(article, nom):
	if nom[0].lower() in "aeiouy":
		return article[:-1] + "'" + nom
	else:
		return article + ' ' + nom


def sessions_after(sessions, session):
	try:
		i = sessions.index(session)
		return sessions[i+1:]+sessions[:i]
	except Exception, e:
		logger.error(u'Unknown session "%s"\n%s' % (session.title, unicode(e)))
		return []



JINJA_FILTERS = {'apostrophe': apostrophe, 'sessions_after': sessions_after, 'slugify': slugify}

STATIC_PATHS = ['programme', 'images']

TEMPLATE_PAGES = {
    'js/custom.js': 'theme/js/custom.js',
    'programme_2014.html': 'programme_2014.html',
    'pitchs-video.html': 'pitchs-video.html',
    'slides-des-sessions.html': 'slides-des-sessions.html',
    }

#TEMPLATE_PAGES = {'programme.html':'programme.html', 'livret.html': 'livret.html', 'sessions.html': 'sessions.html'}

FILES_TO_COPY = (('extra/favicon.ico', 'favicon.ico'),)

NUM_RECENT_POSTS = 10
