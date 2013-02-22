#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2.ext import loopcontrols

AUTHOR = u"L'équipe d'organisation"
SITENAME = u'Agile France 2013'
SITEURL = ''
TWITTER_USERNAME = "AgileFrance"
TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'fr'

MENUITEMS = [
	(u'Inscription', '/index.html'),
	(u'Appel à Orateurs', '/orateur.html'),
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
