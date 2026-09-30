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

    def test_get_siblings(self):
        self.defaultLayoutSetup()
        url = 'index'
        path_info = self.path_manager.get_path_info_from_url(url)
        print(f"\nPathInfo of {url} = {path_info}")
        self.assertIsNotNone(path_info, "get_path_info_from_url should NOT return None")
        self.assertIsNotNone(path_info.path_on_disk, "get_path_info_from_url should NOT return a PathInfo with path_on_disk None")
        sibling_paths: list[tuple[PathInfo, bool]] = self.path_manager.get_sibling_paths(path_info)

        print("\nSiblings START")
        for sibling_path in sibling_paths:
            print(str(sibling_path))
        print("Siblings END")
        self.assertEqual(2, len(sibling_paths), "There should be one sibling path")

    def test_folder_level1_without_index(self):
        urls = [
            '/level1/level11/index.md',
            '/level1/level12/index.md',
            '/level1/level13/index.md',
            '/level1/level14/index.md',
        ]
        for url in urls:
            self.ensure_file_presence(url)

        self.print_folder_structure()
        path_info = self.path_manager.get_path_info_from_url("/level1/")
        sibling_paths: list[tuple[PathInfo, bool]] = self.path_manager.get_sibling_paths(path_info)
        self.assertEqual(4, len(sibling_paths), "There should be 4 sibling paths")

    def test_get_siblings_for_depth_2_with_index(self):
        url1 = '/toto/tutu/index'
        url2 = '/toto/tutu/second'

        self.print_folder_structure()

        self.ensure_file_presence(url1 + ".md")
        self.ensure_file_presence(url2 + ".md")
        path_info1 = self.path_manager.get_path_info_from_url(url1)
        path_info2 = self.path_manager.get_path_info_from_url(url2)

        sibling_paths: list[tuple[PathInfo, bool]] = self.path_manager.get_sibling_paths(path_info1)
        self.assertEqual(2, len(sibling_paths), "There should be one sibling path + itself")
        self.assertEqual(path_info1, sibling_paths[1][0])
        self.assertTrue(sibling_paths[1][1])
        self.assertEqual(path_info2, sibling_paths[0][0])
        self.assertFalse(sibling_paths[0][1])

        print("\nSiblings START")
        for sibling_path in sibling_paths:
            print(str(sibling_path))
        print("Siblings END")
        # self.assertEqual(, len(sibling_paths), "There should be one sibling path + itself")

    def test_get_siblings_for_depth_2_without_index(self):
        url1 = '/toto/tutu/ind1'
        url2 = '/toto/tutu/ind2'
        self.ensure_file_presence(url1 + ".md")
        self.ensure_file_presence(url2 + ".md")

        self.print_folder_structure()

        path_info1 = self.path_manager.get_path_info_from_url(url1)
        path_info2 = self.path_manager.get_path_info_from_url(url2)

        sibling_paths: list[tuple[PathInfo, bool]] = self.path_manager.get_sibling_paths(path_info1)
        self.assertEqual(2, len(sibling_paths), "There should be one sibling path + itself")
        self.assertEqual(path_info1, sibling_paths[1][0])
        self.assertTrue(sibling_paths[1][1])
        self.assertEqual(path_info2, sibling_paths[0][0])
        self.assertFalse(sibling_paths[0][1])

        print("\nSiblings START")
        for sibling_path in sibling_paths:
            print(str(sibling_path))
        print("Siblings END")

    def test_get_siblings_for_root__without_index(self):
        self.defaultLayoutSetup()

        url0 = '/'
        url1 = '/toto/ind1'
        url2 = '/tutu/ind2'
        self.ensure_file_presence(url1 + ".md")
        self.ensure_file_presence(url2 + ".md")

        self.print_folder_structure()

        path_info0: PathInfo = self.path_manager.get_path_info_from_url(url0)
        path_info_toto: PathInfo = self.path_manager.get_path_info_from_url("/toto/")

        sibling_paths: list[tuple[PathInfo, bool]] = self.path_manager.get_sibling_paths(path_info0)
        print("\nSiblings START")
        for sibling_path in sibling_paths:
            print(str(sibling_path))
        print("Siblings END")

        self.assertEqual(4, len(sibling_paths), "There should be 5 sibling path + itself")
        self.assertEqual(path_info_toto, sibling_paths[3][0])
        #self.assertTrue(sibling_paths[1][1])

    def test_relative(self):
        sub_path = Path("/toto/tutu/titi.md")
        base = Path("/toto/")
        self.assertTrue(sub_path.is_relative_to(base))
        print(f"\n#{sub_path.relative_to(base).parts}#")


if __name__ == '__main__':
    unittest.main()
