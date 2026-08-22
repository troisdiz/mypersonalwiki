from dataclasses import dataclass
from pathlib import Path

import frontmatter
import markdown
from markdown.extensions.codehilite import CodeHiliteExtension

from gitwiki.extensions.gitwikilinks import GitWikiLinkExtension
from gitwiki.extensions.gitwikimaths import GitWikiMathJaxExtension
from gitwiki.extensions.gitwikimermaid import GitWikiMermaidExtension
from gitwiki.extensions.gitwikitoc import GitWikiTocExtension


@dataclass
class RenderedPage:
    title: str
    toc: str
    html: str


class PageRenderer:

    def __init__(self, base_url: str, base_pages_path: str):
        self.base_url = base_url
        self.base_pages_path = base_pages_path
        self.toc_ext = GitWikiTocExtension()

    def render_page(self, path_on_disk: Path) -> RenderedPage:
        print(f"Rendering page at path: {path_on_disk}")
        with path_on_disk.open(mode="r", encoding="utf-8") as input_file:
            metadata, content = frontmatter.parse(input_file.read())

        html_content = markdown.markdown(content, extensions=[CodeHiliteExtension(cssclass='codehilite card', linenums=True),
                                                           'markdown.extensions.fenced_code',
                                                           self.toc_ext,
                                                           GitWikiLinkExtension(base_url=self.base_url,
                                                                                end_url=''),
                                                           GitWikiMermaidExtension(),
                                                           GitWikiMathJaxExtension()])
        toc_content = self.toc_ext.toc
        if "title" in metadata:
            title = str(metadata['title'])
        else:
            title = ""
        return RenderedPage(title, toc_content, html_content)

    def render_folder_without_index(self, path_on_disk: Path) -> RenderedPage:
        return RenderedPage("Temp title", "toc_content", "html_content")
