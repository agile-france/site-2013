from pelican import signals
from pelican.readers import MarkdownReader

# Create a new reader class, inheriting from the pelican.reader.MarkdownReader
class SessionMarkdownReader(BaseReader):
    """Reader for Markdown files"""

    enabled = bool(Markdown)
    file_extensions = ['md', 'markdown', 'mkd', 'mdown']

    def __init__(self, *args, **kwargs):
        super(SessionMarkdownReader, self).__init__(*args, **kwargs)
        self.extensions = list(self.settings['MD_EXTENSIONS'])
        if 'meta' not in self.extensions:
            self.extensions.append('meta')

    def _parse_metadata(self, meta):
        """Return the dict containing document metadata"""
        output = {}
        for name, value in meta.items():
            name = name.lower()
            if (name == "summary") or (name == "goal"):
                item_values = "\n".join(value)
                # reset the markdown instance to clear any state
                self._md.reset()
                item = self._md.convert(item_values)
                output[name] = self.process_metadata(name, item)
            else:
                output[name] = self.process_metadata(name, value[0])
        return output

    def read(self, source_path):
        """Parse content and metadata of markdown files"""

        self._md = Markdown(extensions=self.extensions)
        with pelican_open(source_path) as text:
            content = self._md.convert(text)

        metadata = self._parse_metadata(self._md.Meta)
        return content, metadata

def add_reader(readers):
    readers.reader_classes['md'] = SessionMarkdownReader

# This is how pelican works.
def register():
    signals.readers_init.connect(add_reader)
