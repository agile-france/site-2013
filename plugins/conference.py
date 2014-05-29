from collections import defaultdict, namedtuple
from datetime import timedelta
from pelican import signals
from pelican.generators import Generator
from pelican.contents import Page, Static, is_valid_content 
from pelican.readers import read_file
from pelican.utils import path_to_url, slugify, mkdir_p, strftime, get_date
from itertools import chain

import logging
import os
import shutil

logger = logging.getLogger(__name__)


def split_and_strip(map, key):
    if key in map:
        map[key] = [e.strip() for e in map[key].split(',')]


class Session(Page):
    mandatory_properties = ('title', 'duration', 'format', 'speakers')
    default_template = 'session'


    def __init__(self, content, metadata=None, **kwargs):
        if metadata is None:
            metadata = {}
        if not 'summary' in metadata:
            if 'teaser' in metadata:
                metadata['summary'] = metadata['teaser']
            elif 'goal' in metadata:
                metadata['summary'] = metadata['goal']
        super(Session, self).__init__(content, metadata, **kwargs)

        has_duration = hasattr(self, 'duration')
        has_start_date = hasattr(self, 'start_date')

        if has_duration:
            d = self.duration.split(' ')
            if len(d) <> 2 or d[1] <> "minutes":
                logger.error("Unknown duration format: %s", self.duration)
            self.duration = timedelta(minutes=int(d[0]))

        if has_start_date:
            self.start_date = get_date(self.start_date)
            self.locale_start_date = strftime(self.start_date, "%A %d")
            self.locale_start_time = strftime(self.start_date, "%H:%M")

        if has_duration and has_start_date:
            self.end_date = self.start_date + self.duration
            self.locale_end_time = strftime(self.end_date, "%H:%M")

        if not hasattr(self, 'speakers'):
            self.speakers = []
        if not hasattr(self, 'bios'):
            bios = conference.bios.by_role_and_slug['speaker']
            self.bios = []
            for speaker in self.speakers:
                slug = slugify(speaker)
                self.bios.append(slug)
                if slug not in bios:
                    bio = Bio("", {'title': speaker}, settings=self.settings,
                                source_path="", context=self._context)
                    conference.add_bio(bio)

class Bio(Page):
    mandatory_properties = ('title',)
    default_template = 'resume'

    def __init__(self, *args, **kwargs):
        super(Bio, self).__init__(*args, **kwargs)

        if not hasattr(self, 'roles'):
            self.roles = ['speaker']

        if not hasattr(self, 'surname'):
            self.surname = self.title.split(' ')[0]

    def has_page(self):
        return self.content.strip() or (conference.sessions.by_speaker[self.slug])

class BioPic(Static):
    pass


def obj(name, **kwargs):
    return namedtuple(name, kwargs)(**kwargs)


class Conference:
    """All informations about sessions"""

    def __init__(self, *args, **kwargs):
        self.sessions = obj('sessions',
            all = [],
            by_speaker = defaultdict(list),
            by_tag = defaultdict(list))
        self.bios = obj('bios',
            by_role_and_slug = defaultdict(dict),
            by_slug = {})
        self.bio_pics = {}

    def add_bio(self, bio):
        self.bios.by_slug[bio.slug] = bio
        for role in bio.roles:
            self.bios.by_role_and_slug[role][bio.slug] = bio

    def add_session(self, session):
        self.sessions.all.append(session)

        for speaker in session.speakers:
            self.sessions.by_speaker[slugify(speaker)].append(session)

conference = Conference()


class SessionGenerator(Generator):
    """Generate sessions"""

    def __init__(self, *args, **kwargs):
        self.conference = conference
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
                split_and_strip(metadata, 'speakers')
                split_and_strip(metadata, 'bios')
            except Exception, e:
                logger.error(u'Could not process %s\n%s' % (f, unicode(e)))
                continue
            session = Session(content, metadata, settings=self.settings,
                        source_path=f, context=self.context)
            if not is_valid_content(session, f):
                continue

            self.add_source_path(session)

            if session.status == "published":
                if hasattr(session, 'tags'):
                    for tag in session.tags:
                        conference.sessions.by_tag[tag].append(session)
                conference.add_session(session)
            elif session.status == "draft":
                self.drafts.append(session)
            else:
                logger.error(u"Unknown status %s for file %s, skipping it." %
                               (repr(unicode.encode(session.status, 'utf-8')),
                                repr(f)))

        self.context['CONFERENCE'] = self.conference

    def generate_output(self, writer):
        for session in conference.sessions.all:
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
        super(BioGenerator, self).__init__(*args, **kwargs)
        signals.pages_generator_init.send(self)

    def generate_context(self):
        for f in self.get_files(
                os.path.join(self.path, self.settings['BIO_DIR']),
                exclude=self.settings['BIO_EXCLUDES']):
            try:
                content, metadata = read_file(f, settings=self.settings)
                split_and_strip(metadata, 'roles')
            except Exception, e:
                logger.warning(u'Could not process %s\n%s' % (f, str(e)))
                continue
            bio = Bio(content, metadata, settings=self.settings,
                        source_path=f, context=self.context)
            if not is_valid_content(bio, f):
                continue

            self.add_source_path(bio)

            conference.add_bio(bio)

    def generate_output(self, writer):
        for bio in conference.bios.by_slug.values():
            writer.write_file(bio.save_as, self.get_template(bio.template),
                    self.context, bio=bio,
                    relative_urls=self.settings.get('RELATIVE_URLS'))


class BioPicGenerator(Generator):
    def _copy_paths(self, paths, source, destination, output_path,
            final_path=None):
        """Copy all the paths from source to destination"""
        for path in paths:
            copy(path, source, os.path.join(output_path, destination),
                 final_path, overwrite=True)

    def generate_context(self):
        bio_pic_path = self.settings['BIO_PIC_PATH']
        for f in self.get_files(
                os.path.join(self.path, bio_pic_path), extensions=False):
            f_rel = os.path.relpath(f, self.path)
            content, metadata = read_file(
                f, fmt='static', settings=self.settings)
            basename = os.path.splitext(os.path.basename(f))[0]
            metadata['save_as'] = f_rel
            metadata['url'] = path_to_url(metadata['save_as'])
            metadata['slug'] = slugify(basename)
            sc = BioPic(
                content=None,
                metadata=metadata,
                settings=self.settings,
                source_path=f_rel)
            conference.bio_pics[sc.slug] = sc
            self.add_source_path(sc)

    def generate_output(self, writer):
        for sc in conference.bio_pics.values():
            source_path = os.path.join(self.path, sc.source_path)
            save_as = os.path.join(self.output_path, sc.save_as)
            mkdir_p(os.path.dirname(save_as))
            shutil.copy(source_path, save_as)
            logger.info('copying {} to {}'.format(sc.source_path, sc.save_as))


def get_generators(generators):
    return [SessionGenerator, BioGenerator, BioPicGenerator]


def register():
    signals.get_generators.connect(get_generators)
