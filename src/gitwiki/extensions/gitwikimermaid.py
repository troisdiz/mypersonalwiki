from typing import Any

import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class MermaidPreprocessor(Preprocessor):

    def run(self, lines: list[str]) -> list[str]:

        in_mermaid_block: bool = False
        mermaid_lines: list[str] = []

        for (line_num, line) in enumerate(lines):
            if line.startswith('```mermaid'):
                in_mermaid_block = True
                mermaid_lines.append("<div class=\"mermaid\">")
            elif line.startswith('```'):
                in_mermaid_block = False
                mermaid_lines.append("</div>")
            else:
                mermaid_lines.append(line)

        return mermaid_lines


class GitWikiMermaidExtension(Extension):

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(**kwargs)
        self.md = None

    def extendMarkdown(self, md) -> None:
        self.md = md
        md.preprocessors.register(MermaidPreprocessor(md), 'mermaid_preprocessor', 50)


def makeExtension(**kwargs: dict[str, Any]) -> GitWikiMermaidExtension:
    return GitWikiMermaidExtension(**kwargs)