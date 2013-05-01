from collections import defaultdict
from pelican import signals
from pelican.generators import Generator
from pelican.contents import Page, Static, is_valid_content 
from pelican.readers import read_file
from pelican.utils import path_to_url, process_translations, slugify, mkdir_p
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


class Bio(Page):
    default_template = 'bio'


class BioPic(Static):
    pass


class Conference:
    """All informations about sessions"""

    def __init__(self, *args, **kwargs):
        self.sessions = []
        self.tags = defaultdict(list)
        self.bios = defaultdict(dict)
        self.bio_pics = {}
        self.all_bios = {}


    def add_bio(self, bio):
        conference.all_bios[bio.slug] = bio
        for role in bio.roles:
            conference.bios[role][bio.slug] = bio

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
        bios = conference.bios['speaker']
        for f in self.get_files(
                os.path.join(self.path, self.settings['SESSION_DIR']),
                exclude=self.settings['SESSION_EXCLUDES']):
            try:
                content, metadata = read_file(f, settings=self.settings)
                split_and_strip(metadata, 'speakers')
                split_and_strip(metadata, 'bios')
            except Exception, e:
                logger.warning(u'Could not process %s\n%s' % (f, str(e)))
                continue
            session = Session(content, metadata, settings=self.settings,
                        source_path=f, context=self.context)
            if not is_valid_content(session, f):
                continue

            self.add_source_path(session)

            if not hasattr(session, 'bios'):
                session.bios = []
                for speaker in session.speakers:
                    slug = slugify(speaker)
                    session.bios.append(slug)
                    if slug not in bios:
                        bio = Bio("", {'title': speaker, 'roles': ["speaker"]}, settings=self.settings,
                                    source_path="", context=self.context)
                        conference.add_bio(bio)

            if session.status == "published":
                if hasattr(session, 'tags'):
                    for tag in session.tags:
                        conference.tags[tag].append(session)
                all_sessions.append(session)
            elif session.status == "draft":
                self.drafts.append(session)
            else:
                logger.warning(u"Unknown status %s for file %s, skipping it." %
                               (repr(unicode.encode(session.status, 'utf-8')),
                                repr(f)))

        conference.sessions, self.translations = process_translations(all_sessions)

        self.context['CONFERENCE'] = self.conference

    def generate_output(self, writer):
        for session in chain(self.translations, conference.sessions):
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

            if not hasattr(bio, 'roles'):
                bio.roles = ['speaker']
            self.add_source_path(bio)

            conference.add_bio(bio)

    def generate_output(self, writer):
        for bio in conference.all_bios.values():
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
