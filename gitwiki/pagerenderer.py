import codecs
from markdown.extensions.wikilinks import WikiLinkExtension
import markdown
from gitwiki.urlbuilder import url_builder
from gitwiki.extensions.gitwikilinks import GitWikiLinkExtension


class PageRenderer:

    def __init__(self, base_pages_path):
        self.base_pages_path = base_pages_path

    def render_page(self, path_on_disk):
        input_file = codecs.open(path_on_disk, mode="r", encoding="utf-8")
        text = input_file.read()
        html_content = markdown.markdown(text, extensions=['markdown.extensions.codehilite',
                                                           'markdown.extensions.toc',
                                                           GitWikiLinkExtension(base_url='/pages/',
                                                                                end_url='.md')])
        return html_content
