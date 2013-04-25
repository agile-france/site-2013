from collections import defaultdict
from pelican import signals
from pelican.generators import Generator
from pelican.contents import Page, is_valid_content 
from pelican.readers import read_file
from pelican.utils import process_translations
from itertools import chain

import os
import logging

logger = logging.getLogger(__name__)


class Session(Page):
    mandatory_properties = ('title', 'duration', 'format', 'speakers')
    default_template = 'session'


class Bio(Page):
    default_template = 'bio'


class Sessions:
    """All informations about sessions"""

    def __init__(self, *args, **kwargs):
        self.sessions = []
        self.tags = defaultdict(list)

class SessionGenerator(Generator):
    """Generate sessions"""

    def __init__(self, *args, **kwargs):
        self.sessions = Sessions()
        self.drafts = []
        super(SessionGenerator, self).__init__(*args, **kwargs)
        signals.pages_generator_init.send(self)

    def generate_context(self):
        all_sessions = []
        for f in self.get_files(
                os.path.join(self.path, self.settings['SESSION_DIR']),
                exclude=self.settings['SESSION_EXCLUDES']):
            try:
                content, metadata = read_file(f, settings=self.settings)
                metadata['speakers'] = [s.strip() for s in metadata['speakers'].split(',')]
            except Exception, e:
                logger.warning(u'Could not process %s\n%s' % (f, str(e)))
                continue
            session = Session(content, metadata, settings=self.settings,
                        source_path=f, context=self.context)
            if not is_valid_content(session, f):
                continue

            self.add_source_path(session)

            if session.status == "published":
                if hasattr(session, 'tags'):
                    for tag in session.tags:
                        self.sessions.tags[tag].append(session)
                all_sessions.append(session)
            elif session.status == "draft":
                self.drafts.append(session)
            else:
                logger.warning(u"Unknown status %s for file %s, skipping it." %
                               (repr(unicode.encode(session.status, 'utf-8')),
                                repr(f)))

        self.sessions.sessions, self.translations = process_translations(all_sessions)

        self._update_context(('sessions', ))
        self.context['SESSIONS'] = self.sessions

    def generate_output(self, writer):
        for session in chain(self.translations, self.sessions.sessions):
            writer.write_file(session.save_as, self.get_template(session.template),
                    self.context, session=session,
                    relative_urls=self.settings.get('RELATIVE_URLS'))
        for session in self.drafts:
            writer.write_file('drafts/%s' % session.save_as, self.get_template(session.template),
                    self.context, session=session,
                    relative_urls=self.settings.get('RELATIVE_URLS'))

class BioGenerator(Generator):
    """Generate bios"""

    def __init__(self, *args, **kwargs):
        self.bios = {}
        super(BioGenerator, self).__init__(*args, **kwargs)
        signals.pages_generator_init.send(self)

    def generate_context(self):
        all_bios = []
        for f in self.get_files(
                os.path.join(self.path, self.settings['BIO_DIR']),
                exclude=self.settings['BIO_EXCLUDES']):
            try:
                content, metadata = read_file(f, settings=self.settings)
            except Exception, e:
                logger.warning(u'Could not process %s\n%s' % (f, str(e)))
                continue
            bio = Bio(content, metadata, settings=self.settings,
                        source_path=f, context=self.context)
            if not is_valid_content(bio, f):
                continue

            self.add_source_path(bio)

            all_bios.append(bio)

        bios, self.translations = process_translations(all_bios)
        self.bios = {s.slug: s for s in bios}
        self._update_context(('bios', ))
        self.context['BIOS'] = self.bios

    def generate_output(self, writer):
        for bio in chain(self.translations, self.bios.values()):
            writer.write_file(bio.save_as, self.get_template(bio.template),
                    self.context, bio=bio,
                    relative_urls=self.settings.get('RELATIVE_URLS'))


def get_generators(generators):
    return [SessionGenerator, BioGenerator]


def register():
    signals.get_generators.connect(get_generators)
