from typing import Any

import re

from xml.etree.ElementTree import Element
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.treeprocessors import Treeprocessor

CLASS_MARKER = "code_highlight"


class GitwikiHighlightingPreprocessor(Preprocessor):

    def run(self, lines: list[str]) -> list[str]:
        print("GitwikiHighlightingPreprocessor: enter")
        print(lines)
        in_code_block: bool = False
        code_lines: list[str] = []

        for (line_num, line) in enumerate(lines):
            print(f"In line {line_num}: #{line}#")
            if line.startswith('```python'):
                print("In code block")
                in_code_block = True
                code_lines.append(f"<div class=\"{CLASS_MARKER}\">")
            elif in_code_block and line.startswith('```'):
                in_code_block = False
                code_lines.append("</div>")
            else:
                code_lines.append(line)

        return code_lines


class GitwikiHighlightingTreeprocessor(Treeprocessor):

    def run(self, root: Element) -> None:
        """ Find code blocks and store in `htmlStash`. """
        blocks = root.iter('div')
        for block in blocks:
            if block.get('class') == CLASS_MARKER:
                # local_config = self.config.copy()
                text = block[0].text
                if text is None:
                    continue
                placeholder = self.md.htmlStash.store(text)
                # Clear code block in `eTree` instance
                block.clear()


class GitWikiHighlightingExtension(Extension):

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.md = None
        print("GitWikiHighlightingExtension: initialized")

    def extendMarkdown(self, md) -> None:
        self.md = md
        md.preprocessors.register(GitwikiHighlightingPreprocessor(md), 'gitwiki_highlighting_preprocessor', 10)
        md.treeprocessors.register(GitwikiHighlightingTreeprocessor(md), 'gitwiki_highlighting_treeprocessor', 30)
        print("GitWikiHighlightingExtension: extendMarkdown")


def makeExtension(**kwargs: dict[str, Any]) -> GitWikiHighlightingExtension:
    return GitWikiHighlightingExtension(**kwargs)
