import unittest
import markdown
from gitwiki.extensions.gitwikilinks import GitWikiLinkExtension
from gitwiki.extensions.gitwikitoc import TocExtension

# [TOC]

text = """
# Titre 1
## Titre 1.2
# Titre 2"""


class TestGitWikiPathUrls(unittest.TestCase):

    def test(self):
        toc_ext = TocExtension()
        html_content = markdown.markdown(text, extensions=['markdown.extensions.codehilite',
                                                           'markdown.extensions.toc',
                                                           GitWikiLinkExtension(base_url='/pages/',
                                                                                end_url=''),
                                                           toc_ext])

        self.assertIsNotNone(toc_ext.toc)
        print(toc_ext.toc)
