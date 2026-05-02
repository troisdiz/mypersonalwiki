from __future__ import annotations
from os.path import join
from os.path import exists
from pathlib import Path
from urllib import parse
from enum import Enum
from enum import unique
from functools import cmp_to_key
from pathlib import Path

from jinja2 import Environment, PackageLoader

INDEX_FILE_NAME = 'index.md'
SIDEBAR_FILE_NAME = '__sidebar.md'
URL_CHARACTER_SEPARATOR = '/'


@unique
class PathNature(Enum):
    not_found = 0
    other_resource_not_found = 1
    md_file = 2  # to be rendered as html (otherwise, use other_resource_file
    other_resource_file = 3
    folder_without_index = 4
    folder_with_index = 5
    sidebar = 6  # TODO use it!

    def can_have_children(self) -> bool:
        return self.value > PathNature.other_resource_file.value


class PathInfo:
    def __init__(self, path_nature: PathNature, path_on_disk: Path | None, url_items: list[str] = None):
        if path_on_disk is None:
            raise Exception(f"cannot create PathInfo because path_on_disk is None (url_items = {str(url_items)}")

        self.pathNature: PathNature = path_nature
        self.path_on_disk: Path = path_on_disk
        # TODO
        if url_items is None:
            self.url_items = []
        else:
            self.url_items = url_items

    def __str__(self) -> str:
        if self.path_on_disk is not None:
            path_on_disk_str = self.path_on_disk
        else:
            path_on_disk_str = 'N/A'
        return f"{self.pathNature} [{path_on_disk_str}] / url items {self.url_items}"

    def name(self):
        return self.url_items[-1]

    def is_root(self):
        return len(self.url_items) == 0

    def parent(self) -> PathInfo:
        if self.is_root():
            raise Exception(f"{self} is a root path")
        return PathInfo(path_nature=PathNature.folder_without_index,
                        path_on_disk=self.path_on_disk.parent,
                        url_items=self.url_items[:-1])


def path_info_child_of(parent: PathInfo, child_name: str) -> PathInfo:
    if not parent.pathNature.can_have_children():
        raise Exception(f"{parent} of nature {parent.pathNature} can't have children (proposed child is {child_name})")
    return PathInfo(path_nature=None,
                    path_on_disk=parent.path_on_disk / child_name,
                    url_items=parent.url_items + [child_name])


class MalFormedGitWikiUrl(Exception):

    def __init__(self, message):
        self.message = message


# class GitWikiUrl:
#     # 2 subslasses (abs and rel ?)
#     def __init__(self, is_absolute, path_elements):
#         self.is_absolute = is_absolute
#         self.path_elements = path_elements
#
#     def canonize(self) -> 'GitWikiUrl':
#         path_elements = self.path_elements
#         while True:
#             try:
#                 index = path_elements.index('..')
#                 if index <= 0:
#                     if self.is_absolute:
#                         raise MalFormedGitWikiUrl('Too much ..')
#                     else:
#                         break
#                 path_elements = path_elements[:index - 1] + path_elements[index + 1:]
#             except ValueError:
#                 break
#         return GitWikiUrl(self.is_absolute, path_elements)

class TemplateManager:
    def __init__(self, templates_base_path: Path):
        self.templates_path = join(templates_base_path, 'templates')
        loader = PackageLoader("gitwiki", "templates")
        self.jinja_env = Environment(
            loader=loader,
        )

    def get_templates_path(self):
        """
        Path for the templates folder (it contains both the Jinja template and the static generic files to far)
        # TODO: shouldn't Jinja templates and static files be in different folders?
        :return:
        """
        return self.templates_path

    def get_jinja_template(self, template_name):
        return self.jinja_env.get_template(template_name)


class PathManager:
    """
    PathManager is responsible for managing paths in gitwiki

    """

    def __init__(self, base_path: Path):
        """
        Creates a PathManager instance

        :param base_path: The root of the wiki repository, where the pages and other assets are stored
        """

        self.base_pathlib_path = base_path

    def get_sidebar_path(self, page_path: str) -> str | None:
        """t
        Returns the path to the sidebar source by looking in the current page folder and going up

        :return: The path to the sidebar source
        """
        page_pathlib_path = Path(page_path)
        current_page = page_pathlib_path.parent
        while current_page.is_subpath_of(self.base_pathlib_path):
            if current_page.contains(SIDEBAR_FILE_NAME):
                return str((current_page / SIDEBAR_FILE_NAME).absolute())
            current_page = current_page.parent
        return None

    def get_sibling_paths(self, path_info: PathInfo) -> list[PathInfo]:
        # if not path_info.pathNature.can_have_children():
        #     raise Exception(f"{path_info} of nature {path_info.pathNature} can't have children")

        source_path = path_info.path_on_disk
        children = [item for item in source_path.parent.iterdir()]

        # dir

        def compare_func(p1: Path, p2: Path):
            if p1.is_dir() and p2.is_dir():
                return p1.name > p2.name
            elif p1.is_file() and p2.is_file():
                return p1.name > p2.name
            elif p1.is_file() and p2.is_dir():
                return -1
            else:
                return 1

        sorted_children = sorted(children, key=cmp_to_key(compare_func))
        # files
        sibling_path_infos = [
            path_info_child_of(path_info.parent(), child.name)
            for child in sorted_children
        ]

        folder_and_pages = [
            path_info
            for path_info in sibling_path_infos
            if (path_info.path_on_disk != source_path) and
               (
                       path_info.pathNature == PathNature.folder_with_index
                       or path_info.pathNature == PathNature.folder_without_index
                       or path_info.pathNature == PathNature.md_file
               )
        ]

        return folder_and_pages

    def get_parent_path_info(self, path_info: PathInfo) -> PathInfo:
        if path_info.path_on_disk == self.base_pathlib_path:
            # Prevent going below the root
            return None
        return PathInfo(PathNature.folder_with_index, path_info.path_on_disk.parent, path_info.url_items[-1])

    def _contains_index(self, path: Path) -> bool:
        return self._exists_on_disk(path / INDEX_FILE_NAME)

    def _exists_on_disk(self, path: Path) -> bool:
        # TODO already includes base_path ?
        return path.exists()

    def get_path_info_from_url(self, raw_url_path: str) -> PathInfo:
        # TODO portability because of separator
        # TODO handle .md files extensions
        # TODO handle folders which should default to index.md
        # TODO Create object to handle this stuff and make it testable

        decoded_url_path = parse.unquote(raw_url_path)
        raw_path_elts = decoded_url_path.split(URL_CHARACTER_SEPARATOR)

        # Variables introduced to iterate (see below)
        unslashed_decoded_url_path = decoded_url_path
        cleaned_path_elts = raw_path_elts

        # if url starts with splash, remove it
        if raw_path_elts[0] == '':
            unslashed_decoded_url_path: str = decoded_url_path[1:]
            cleaned_path_elts = raw_path_elts[1:]

        # test is true if last char is '/' and then split returns empty
        # string at the end
        if raw_path_elts[-1] == '':
            # Folder case
            path_nature = None
            if self._exists_on_disk(self.base_pathlib_path / unslashed_decoded_url_path):
                if self._contains_index(self.base_pathlib_path / unslashed_decoded_url_path):
                    path_nature = PathNature.folder_with_index
                else:
                    path_nature = PathNature.folder_without_index
            else:
                path_nature = PathNature.not_found
            return PathInfo(path_nature=path_nature,
                            # TODO suspicious when there is no index!!!
                            path_on_disk=self.base_pathlib_path / unslashed_decoded_url_path / INDEX_FILE_NAME,
                            url_items=cleaned_path_elts)

        # File case : look for extension
        last_elt = raw_path_elts[-1]
        file_parent_url_items = cleaned_path_elts[:-1]
        file_elts = last_elt.split('.')
        extension = file_elts[-1]
        if len(file_elts) == 1:
            # No extension
            path_nature = None
            potential_md_path = self.base_pathlib_path / f"{unslashed_decoded_url_path}.md"
            if potential_md_path.exists():
                return PathInfo(path_nature=PathNature.md_file,
                                path_on_disk=Path(potential_md_path),
                                url_items=cleaned_path_elts)
            else:
                return PathInfo(path_nature=PathNature.not_found,
                                path_on_disk=None,
                                url_items=cleaned_path_elts)
        else:
            absolute_md_path = self.base_pathlib_path / unslashed_decoded_url_path
            if absolute_md_path.exists():
                return PathInfo(path_nature=PathNature.other_resource_file,
                                path_on_disk=absolute_md_path,
                                url_items=file_parent_url_items)
            else:
                return PathInfo(path_nature=PathNature.other_resource_not_found,
                                path_on_disk=None,
                                url_items=file_parent_url_items)


def find_extension(url):
    reversed_url = url.reverse
    extension = ''
    for char in reversed_url:
        if char == '.':
            return extension.reverse
        elif char == '/':
            return None
        else:
            extension += char

    return None
