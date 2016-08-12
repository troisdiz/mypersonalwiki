import unittest
from gitwiki.breadcrumbrenderer import BreacrumbRender


class TestGitWikiBreadcrumbs(unittest.TestCase):

    def test_build_tuples_empty(self):
        bcr = BreacrumbRender('/pages')
        real = [it for it in bcr.build_tuples([])]
        expected = [(['/pages'], 'Home')]
        self.print_and_assert(real, expected)

    def test_build_tuples_1(self):
        bcr = BreacrumbRender('/pages')
        item_name = 'Item1'
        real = [it for it in bcr.build_tuples([item_name])]
        expected = [(['/pages'], 'Home'), (['/pages', item_name], item_name)]
        self.print_and_assert(real, expected)

    def print_and_assert(self, real, expected):
        print(" / ".join([str(i) for i in real]))
        print(" / ".join([str(i) for i in expected]))
        self.assertListEqual(real, expected)

    def test_render(self):
        bcr = BreacrumbRender('/pages')
        print(bcr.render_path([]))
