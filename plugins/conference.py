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


class Speaker(Page):
    default_template = 'speaker'


class SessionGenerator(Generator):
    """Generate sessions"""

    def __init__(self, *args, **kwargs):
        self.sessions = []
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
                        filename=f, context=self.context)
            if not is_valid_content(session, f):
                continue

            self.add_filename(session)

            if session.status == "published":
                all_sessions.append(session)
            elif session.status == "draft":
                self.drafts.append(session)
            else:
                logger.warning(u"Unknown status %s for file %s, skipping it." %
                               (repr(unicode.encode(session.status, 'utf-8')),
                                repr(f)))

        self.sessions, self.translations = process_translations(all_sessions)

        self._update_context(('sessions', ))
        self.context['SESSIONS'] = self.sessions

    def generate_output(self, writer):
        for session in chain(self.translations, self.sessions):
            writer.write_file(session.save_as, self.get_template(session.template),
                    self.context, session=session,
                    relative_urls=self.settings.get('RELATIVE_URLS'))
        for session in self.drafts:
            writer.write_file('drafts/%s' % session.save_as, self.get_template(session.template),
                    self.context, session=session,
                    relative_urls=self.settings.get('RELATIVE_URLS'))

class SpeakerGenerator(Generator):
    """Generate speakers"""

    def __init__(self, *args, **kwargs):
        self.speakers = {}
        super(SpeakerGenerator, self).__init__(*args, **kwargs)
        signals.pages_generator_init.send(self)

    def generate_context(self):
        all_speakers = []
        for f in self.get_files(
                os.path.join(self.path, self.settings['SPEAKER_DIR']),
                exclude=self.settings['SPEAKER_EXCLUDES']):
            try:
                content, metadata = read_file(f, settings=self.settings)
            except Exception, e:
                logger.warning(u'Could not process %s\n%s' % (f, str(e)))
                continue
            speaker = Speaker(content, metadata, settings=self.settings,
                        filename=f, context=self.context)
            if not is_valid_content(speaker, f):
                continue

            self.add_filename(speaker)

            all_speakers.append(speaker)

        speakers, self.translations = process_translations(all_speakers)
        self.speakers = {s.slug: s for s in speakers}
        self._update_context(('speakers', ))
        self.context['SPEAKERS'] = self.speakers

    def generate_output(self, writer):
        for speaker in chain(self.translations, self.speakers.values()):
            writer.write_file(speaker.save_as, self.get_template(speaker.template),
                    self.context, speaker=speaker,
                    relative_urls=self.settings.get('RELATIVE_URLS'))


def get_generators(generators):
    return [SessionGenerator, SpeakerGenerator]


def register():
    signals.get_generators.connect(get_generators)
