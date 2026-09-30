import unittest
import tempfile
import os
import time
from collections import deque
from pathlib import Path
from tempfile import TemporaryDirectory

from gitwiki.pathmanager import PathManager, PathInfo
from gitwiki.pathmanager import PathNature
from gitwiki.pathmanager import find_extension
from gitwiki.server import BASE_PAGE_URL


class TestGitWikiPathUrls(unittest.TestCase):

    def setUp(self):
        self.temp_dir: TemporaryDirectory = tempfile.TemporaryDirectory("PathManager", "")
        temp_folder = self.temp_dir.name
        self.temp_folder_path = Path(temp_folder)
        self.path_manager = PathManager(self.temp_folder_path, BASE_PAGE_URL)

    def defaultLayoutSetup(self):
        self.ensure_file_presence("index.md")
        self.ensure_file_presence("other.md")
        self.ensure_file_presence("jpeg.jpg")

    def tearDown(self):
        self.temp_dir.cleanup()

    def ensure_file_presence(self, file_path):
        relative_file_path = file_path
        if file_path[0] == '/':
            relative_file_path = file_path[1:]

        full_path = os.path.join(self.temp_dir.name, relative_file_path)
        #print('Temp dir : #' + self.temp_dir.name + '#')
        #print('About to create : #' + full_path + '#')
        basedir = os.path.dirname(full_path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        with open(full_path, 'a'):
            os.utime(full_path, None)

    def print_folder_structure(self):
        print(f"Futur debug tool exploring {self.temp_dir.name}")
        self.print_folder(self.temp_folder_path, 0)

    def print_folder(self, folder: Path, depth: int):

        print(f"{'':{2 * depth}}D {folder.name}")
        sub_files: list[Path] = []
        sub_folders: list[Path] = []
        for item in folder.iterdir():
            if item.is_dir():
                sub_folders.append(item)
            elif item.is_file():
                sub_files.append(item)
            else:
                self.fail(f"Neither folder nor file: {item}")
        for item in sub_folders:
            self.print_folder(item, depth + 1)
        for item in sub_files:
            print(f"{'':{2 * (depth+1)}}F {item.name}")

    def test_path_debug_print(self):
        print()
        url = '/d1/d11/f1.md'
        self.ensure_file_presence(url)
        url = '/d1/d11/f2.md'
        self.ensure_file_presence(url)
        url = '/d1/d12/f3.md'
        self.ensure_file_presence(url)
        url = '/d2/tutu/'
        self.ensure_file_presence(url + 'index.md')
        self.print_folder_structure()

    def test_path_info_from_url_for_folder_with_index(self):
        print()
        url = '/toto/tutu'
        url = '/toto/tutu/'
        self.ensure_file_presence(url + 'index.md')
        self.print_folder_structure()

        path_info: PathInfo = self.path_manager.get_path_info_from_url(url)
        print(f"PathInfo: {path_info}")
        self.assertEqual(self.temp_folder_path / url[1:], path_info.path_on_disk)

    def test_path_info_from_url_for_folder_without_index(self):
        url = '/toto/tutu-no-index/'
        self.ensure_file_presence(url + 'no-index')
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.folder_without_index, path_info.pathNature)

    def test_path_info_from_url_for_root_page(self):
        url = ''
        self.ensure_file_presence('index.md')
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.folder_with_index, path_info.pathNature)
        self.assertEqual(self.temp_folder_path, path_info.path_on_disk)

    def test_path_info_from_url_for_page(self):
        url = "/toto/tutu"
        self.ensure_file_presence(url + '.md')
        path_info = self.path_manager.get_path_info_from_url(url)
        print(f"PathInfo: {path_info}")
        self.assertEqual(self.temp_folder_path / f"{url[1:]}.md", path_info.path_on_disk)

    def test_path_info_from_url_for_page_not_found(self):
        url = '/toto/tutu-not-found'
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.not_found, path_info.pathNature)

    def test_path_info_from_url_for_page_with_space(self):
        url = '/toto/tu%20tu'
        decoded_url = '/toto/tu tu'
        self.ensure_file_presence(decoded_url + '.md')
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(self.temp_folder_path / f"{decoded_url[1:]}.md", path_info.path_on_disk)

    def test_path_info_from_url_for_other_resource(self):
        url = '/test.jpg'
        self.ensure_file_presence(url[1:])
        path_info = self.path_manager.get_path_info_from_url(url)
        print(f"Path = {path_info.path_on_disk}")
        self.assertEqual(self.temp_folder_path / url[1:], path_info.path_on_disk)

    def test_path_info_from_url_for_other_resource_not_found(self):
        url = '/test-not-found.jpg'
        path_info = self.path_manager.get_path_info_from_url(url)
        self.assertEqual(PathNature.other_resource_not_found, path_info.pathNature)

    def test_path_info_from_url_file_with_dots(self):
        file_name = "2020-04-02-PL-0.2.2-security"
        urls = [
            f"{file_name}.md",
        ]
        for url in urls:
            self.ensure_file_presence(url)
        path_info = self.path_manager.get_path_info_from_url(file_name)
        self.assertEqual(PathNature.md_file, path_info.pathNature)


    def test_relative(self):
        sub_path = Path("/toto/tutu/titi.md")
        base = Path("/toto/")
        self.assertTrue(sub_path.is_relative_to(base))
        print(f"\n#{sub_path.relative_to(base).parts}#")


if __name__ == '__main__':
    unittest.main()
