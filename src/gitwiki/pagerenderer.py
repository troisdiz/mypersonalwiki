import codecs
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from gitwiki.extensions.gitwikilinks import GitWikiLinkExtension
from gitwiki.extensions.gitwikitoc import GitWikiTocExtension


class PageRenderer:

    def __init__(self, base_url, base_pages_path):
        self.base_url = base_url
        self.base_pages_path = base_pages_path
        self.toc_ext = GitWikiTocExtension()

    def render_page(self, path_on_disk):
        input_file = codecs.open(path_on_disk, mode="r", encoding="utf-8")
        text = input_file.read()
        html_content = markdown.markdown(text, extensions=[CodeHiliteExtension(cssclass='codehilite card'),
                                                           'markdown.extensions.fenced_code',
                                                           self.toc_ext,
                                                           GitWikiLinkExtension(base_url=self.base_url,
                                                                                end_url='')])
        toc_content = self.toc_ext.toc
        return toc_content, html_content
