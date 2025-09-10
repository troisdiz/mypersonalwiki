import unittest
from gitwiki.breadcrumbrenderer import BreadcrumbRenderer
from gitwiki.breadcrumbrenderer import build_tuples


class TestGitWikiBreadcrumbs(unittest.TestCase):

    def test_build_tuples_empty(self):
        real = [it for it in build_tuples([])]
        expected = [([], 'Home', True)]
        self.print_and_assert(real, expected)

    def test_build_tuples_1(self):
        item_name = 'Item1'
        real = [it for it in build_tuples([item_name])]
        expected = [([], 'Home', True), ([item_name], item_name, False)]
        self.print_and_assert(real, expected)

    def print_and_assert(self, real, expected):
        print(" / ".join([str(i) for i in real]))
        print(" / ".join([str(i) for i in expected]))
        self.assertListEqual(real, expected)

    def test_render(self):
        bcr = BreadcrumbRenderer('/pages/')
        self.assertEqual('<li class="breadcrumb-item">    <a href="/pages/">Home</a></li>',
                         bcr.render_path([]))
