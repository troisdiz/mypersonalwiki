import unittest
import tempfile
import os
import time
from gitwiki.pathmanager import PathManager
from gitwiki.pathmanager import find_extension


class TestGitWikiPathUrls(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory("TestDownloadToday", "")
        self.path_manager = PathManager(self.temp_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_folder_index(self):
        url = "/toto/tutu/"
        path = self.path_manager.get_path_from_url(url)
        print("Path = " + path)
        self.assertEqual(os.path.join(self.temp_dir.name, url, "index.md"), path)

    def test_page(self):
        url = "/toto/tutu"
        path = self.path_manager.get_path_from_url(url)
        self.assertEqual(os.path.join(self.temp_dir.name, url + '.md'), path)

    def test_page_with_space(self):
        url = "/toto/tu%20tu"
        decoded_url = "/toto/tu tu"
        path = self.path_manager.get_path_from_url(url)
        self.assertEqual(os.path.join(self.temp_dir.name, decoded_url + '.md'), path)

    def test_other_resource(self):
        url = '/test.jpg'
        path = self.path_manager.get_path_from_url(url)
        print("Path = " + path)
        self.assertEqual(os.path.join(self.temp_dir.name, url), path)

if __name__ == '__main__':
    unittest.main()
