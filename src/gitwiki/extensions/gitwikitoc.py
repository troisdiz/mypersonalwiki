"""
GitWiki Table of Contents Extension for Python-Markdown
===============================================

Mostly uses <https://Python-Markdown.github.io/extensions/toc> with the goal to externalize the
table of content anywhere we want

But GitWikiTocExtention.extendMarkdown has been copied from originl Python-Markdown project toc extension
"""

from markdown.extensions.toc import TocTreeprocessor, TocExtension


class GitWikiTocTreeprocessor(TocTreeprocessor):
    def __init__(self, md, ext, config):
        super().__init__(md, config)

        self.ext = ext

    def run(self, doc):
        super().run(doc)
        self.ext.toc = self.md.toc


class GitWikiTocExtension(TocExtension):

    TreeProcessorClass = GitWikiTocTreeprocessor

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        self.md = md
        self.reset()
        tocext = self.TreeProcessorClass(md, self, self.getConfigs())
        # Headerid ext is set to '>prettify'. With this set to '_end',
        # it should always come after headerid ext (and honor ids assinged
        # by the header id extension) if both are used. Same goes for
        # attr_list extension. This must come last because we don't want
        # to redefine ids after toc is created. But we do want toc prettified.
        md.treeprocessors.register(tocext, 'toc', 5)


def makeExtension(**kwargs):  # pragma: no cover
    return GitWikiTocExtension(**kwargs)
