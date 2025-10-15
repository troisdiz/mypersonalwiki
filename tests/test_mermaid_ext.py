import os
import unittest

from markdown.extensions.codehilite import CodeHiliteExtension

from gitwiki.extensions.gitwikimermaid import GitWikiMermaidExtension
import markdown


class TestMermaidExtension(unittest.TestCase):

    def run_real_test(self, md_file_name, expected_html_file_name):
        md_file_path = os.path.join(os.path.dirname(__file__), "testdata", md_file_name)
        with open(md_file_path, 'r') as md_file:
            md_file_content = md_file.read()

        expected_html_file_path = os.path.join(os.path.dirname(__file__), "testdata", expected_html_file_name)
        with open(expected_html_file_path, 'r') as expected_html_file:
            expected_html_file_content = expected_html_file.read()

        html_content = markdown.markdown(md_file_content, extensions=[
            GitWikiMermaidExtension(),
        ])

        print(f"\n---\n{html_content}\n---\n")
        self.assertEqual(expected_html_file_content, html_content)

    def test_parse(self):
        self.run_real_test("single-mermaid-block.md", "expected-single-mermaid-block.html")

    def test_parse_two_blocks_mermaid_last(self):
        self.run_real_test("two-code-blocks-mermaid-last.md", "expected-two-code-blocks-mermaid-last.html")

    def test_parse_two_blocks_mermaid_first(self):
        self.run_real_test("two-code-blocks-mermaid-first.md", "expected-two-code-blocks-mermaid-first.html")


if __name__ == '__main__':
    unittest.main()
