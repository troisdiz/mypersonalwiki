from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree
import re

replacements = "".maketrans("àâéèêîôùû", "aaeeeiouu")


def build_url(label, base, end):
    """ Build a url from the label, a base, and an end. """
    no_accent = normalize(label)
    clean_label = re.sub(r'([ ]+_)|(_[ ]+)|([ ]+)', '_', no_accent)
    final_label = clean_label
    # if clean_label.endswith('/'):
    #     final_label = clean_label + "index"

    if final_label.startswith('/'):
        # Absolute url
        return '%s%s%s' % (base, final_label[1:], end)
    else:
        # Relative url
        return '%s%s' % (final_label, end)


def build_url_from_paths(paths, base, is_folder):
    # paths_with_slash = [path + '/' for path in paths]
    # url = build_url('/' + '/'.join(paths_with_slash), base, end)
    url = build_url('/' + '/'.join(paths), base, '')
    if is_folder:
        if url[-1] != '/':
            return url + '/'
    return url


class GitWikiLinkExtension(Extension):

    def __init__(self, *args, **kwargs):
        self.config = {
            'base_url': ['/', 'String to append to beginning or URL.'],
            'end_url': ['/', 'String to append to end of URL.'],
            'html_class': ['wikilink', 'CSS hook. Leave blank for none.'],
            'build_url': [build_url, 'Callable formats URL from label.'],
        }

        super(GitWikiLinkExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        self.md = md

        # append to end of inline patterns
        WIKILINK_RE = r'\[\[([\w0-9_ -\.\/]+)\]\]'
        wikilinkPattern = GitWikiLinks(WIKILINK_RE, self.getConfigs())
        wikilinkPattern.md = md
        md.inlinePatterns.add('wikilink', wikilinkPattern, "<not_strong")


def build_text_link(label):
    return label


def normalize(label):
    """Replace accents with close letter
    Note : use unidecode"""
    return label.translate(replacements)


class GitWikiLinks(Pattern):
    def __init__(self, pattern, config):
        super(GitWikiLinks, self).__init__(pattern)
        self.config = config

    def handleMatch(self, m):
        if m.group(2).strip():
            base_url, end_url, html_class = self._getMeta()
            label = m.group(2).strip()
            url = build_url(label, base_url, end_url)
            a = etree.Element('a')
            a.text = build_text_link(label)
            a.set('href', url)
            if html_class:
                a.set('class', html_class)
        else:
            a = ''
        return a

    def _getMeta(self):
        """ Return meta data or config data. """
        base_url = self.config['base_url']
        end_url = self.config['end_url']
        html_class = self.config['html_class']
        if hasattr(self.md, 'Meta'):
            if 'wiki_base_url' in self.md.Meta:
                base_url = self.md.Meta['wiki_base_url'][0]
            if 'wiki_end_url' in self.md.Meta:
                end_url = self.md.Meta['wiki_end_url'][0]
            if 'wiki_html_class' in self.md.Meta:
                html_class = self.md.Meta['wiki_html_class'][0]
        return base_url, end_url, html_class


def makeExtension(*args, **kwargs):
    return GitWikiLinkExtension(*args, **kwargs)
