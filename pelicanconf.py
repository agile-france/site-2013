#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from jinja2.ext import loopcontrols

AUTHOR = u"L'équipe d'organisation"
SITENAME = u'Agile France 2013'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'fr'

MENU = [
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

DEFAULT_PAGINATION = 10

THEME = 'themes/ericka'

INDEX_SAVE_AS = False

JINJA_EXTENSIONS = [loopcontrols]
