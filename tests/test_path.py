import unittest
import tempfile
import os
import time
from pathlib import Path
from tempfile import TemporaryDirectory

from gitwiki.pathmanager import PathManager, PathInfo
from gitwiki.pathmanager import PathNature
from gitwiki.pathmanager import find_extension


class TestGitWikiPathUrls(unittest.TestCase):

    def setUp(self):
        self.temp_dir: TemporaryDirectory = tempfile.TemporaryDirectory("TestDownloadToday", "")
        temp_folder = self.temp_dir.name
        self.temp_folder_path = Path(temp_folder)
        index_path: Path = self.temp_folder_path / 'index.md'
        index_path.touch()

        jpeg_path: Path = self.temp_folder_path / 'jpeg.jpg'
        jpeg_path.touch()

        program_base_path = os.path.dirname(os.path.realpath(__file__))
        self.path_manager = PathManager(self.temp_folder_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_folder_with_index(self):
        url = '/toto/tutu/'
        self.ensure_file_presence(url + 'index.md')
        path_info = self.path_manager.get_path_info_from_url(url)
        print(f"Path = {path_info.path_on_disk}")
        self.assertEqual(self.temp_folder_path / url[1:], path_info.path_on_disk)

    def test_folder_without_index(self):
        url = '/toto/tutu-no-index/'
        self.ensure_file_presence(url + 'no-index')
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.folder_without_index, path_info.pathNature)

    def test_root_page(self):
        url = ''
        self.ensure_file_presence('index.md')
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.folder_with_index, path_info.pathNature)
        self.assertEqual(self.temp_folder_path, path_info.path_on_disk)

    def test_page(self):
        url = "/toto/tutu"
        self.ensure_file_presence(url + '.md')
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(self.temp_folder_path / f"{url[1:]}.md", path_info.path_on_disk)

    def test_page_not_found(self):
        url = '/toto/tutu-not-found'
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.not_found, path_info.pathNature)

    def test_page_with_space(self):
        url = '/toto/tu%20tu'
        decoded_url = '/toto/tu tu'
        self.ensure_file_presence(decoded_url + '.md')
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(self.temp_folder_path / f"{decoded_url[1:]}.md", path_info.path_on_disk)

    def test_other_resource(self):
        url = '/test.jpg'
        self.ensure_file_presence(url[1:])
        path_info = self.path_manager.get_path_info_from_url(url)
        print(f"Path = {path_info.path_on_disk}")
        self.assertEqual(self.temp_folder_path / url[1:], path_info.path_on_disk)

    def test_other_resource_not_found(self):
        url = '/test-not-found.jpg'
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.other_resource_not_found, path_info.pathNature)

    def test_get_siblings(self):
        url = 'index'
        path_info = self.path_manager.get_path_info_from_url(url)
        print(f"\nPathInfo of {url} = {path_info}")
        self.assertIsNotNone(path_info, "get_path_info_from_url should NOT return None")
        self.assertIsNotNone(path_info.path_on_disk, "get_path_info_from_url should NOT return a PathInfo with path_on_disk None")
        sibling_paths: list[PathInfo] = self.path_manager.get_sibling_paths(path_info)
        print("\nSiblings START")
        for sibling_path in sibling_paths:
            print(str(sibling_path))
        print("Siblings END")

    def ensure_file_presence(self, file_path):
        relative_file_path = file_path
        if file_path[0] == '/':
            relative_file_path = file_path[1:]

        full_path = os.path.join(self.temp_dir.name, relative_file_path)
        print('Temp dir : #' + self.temp_dir.name + '#')
        print('About to create : #' + full_path + '#')
        basedir = os.path.dirname(full_path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        with open(full_path, 'a'):
            os.utime(full_path, None)

if __name__ == '__main__':
    unittest.main()
