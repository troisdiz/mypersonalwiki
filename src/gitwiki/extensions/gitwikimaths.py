import html
from typing import Any

import markdown
from markdown import Markdown
from markdown.inlinepatterns import Pattern

# This is very inspired from https://github.com/mayoff/python-markdown-mathjax/blob/6d6237126e611ab74be8513a42dcdf8336ecc444/mdx_mathjax.py

MATHJAX_RE: str = r'(?<!\\)(\$\$?)(.+?)\2'
# Original priority from Python-Markdown's wikilinks extension
MATHJAX_PATTERN_PRIORITY: float = 100

class GitWikiMathJaxPattern(Pattern):

    def __init__(self, md: Markdown):
        super(GitWikiMathJaxPattern, self).__init__(MATHJAX_RE)
        self.md = md

    def handleMatch(self, m):
        # Pass the math code through, unmodified except for basic entity substitutions.
        # Stored in htmlStash so it doesn't get further processed by Markdown.
        text = html.escape(m.group(2) + m.group(3) + m.group(2), quote=True)
        return self.md.htmlStash.store(text)

class GitWikiMathJaxExtension(markdown.Extension):

    def extendMarkdown(self, md):
        # Needs to come before escape matching because \ is pretty important in LaTeX
        mathjax_pattern = GitWikiMathJaxPattern(md=md)

        md.inlinePatterns.register(mathjax_pattern, 'mathjax', MATHJAX_PATTERN_PRIORITY)

def makeExtension(**kwargs: dict[str, Any]) -> GitWikiMathJaxExtension:
    return GitWikiMathJaxExtension(**kwargs)