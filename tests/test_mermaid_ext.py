import unittest

from gitwiki.extensions.gitwikimermaid import GitWikiMermaidExtension
import markdown

text = """
# Titre 1

```mermaid
graph TB
D --> E
E --> F
```

"""

EXPECTED_MERMAID_HTML = """<h1>Titre 1</h1>
<div class="mermaid">
graph TB
D --> E
E --> F
</div>"""


class TestMermaidExtension(unittest.TestCase):

    def test_parse(self):
        html_content = markdown.markdown(text, extensions=[
            GitWikiMermaidExtension(),
        ])

        print(f"\n---\n{html_content}\n---\n")
        self.assertEqual(EXPECTED_MERMAID_HTML, html_content)  # add assertion here


if __name__ == '__main__':
    unittest.main()
