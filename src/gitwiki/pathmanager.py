from os.path import join
from os.path import exists
from urllib import parse
from enum import Enum
from enum import unique
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


class PathInfo:
    def __init__(self, path_nature: PathNature, path_on_disk: str, url_items: list[str] = None):
        self.pathNature: PathNature = path_nature
        self.path_on_disk: str = path_on_disk
        # TODO
        if url_items is None:
            self.url_items = []
        else:
            self.url_items = url_items

    def __str__(self) -> str:
        if self.path_on_disk is not None:
            path_on_disk = self.path_on_disk
        else:
            path_on_disk = 'N/A'
        return f"{self.pathNature} [{path_on_disk}] / url items {self.url_items}"


class MalFormedGitWikiUrl(Exception):

    def __init__(self, message):
        self.message = message


class GitWikiUrl:
    # 2 subslasses (abs and rel ?)
    def __init__(self, is_absolute, path_elements):
        self.is_absolute = is_absolute
        self.path_elements = path_elements

    def canonize(self) -> 'GitWikiUrl':
        path_elements = self.path_elements
        while True:
            try:
                index = path_elements.index('..')
                if index <= 0:
                    if self.is_absolute:
                        raise MalFormedGitWikiUrl('Too much ..')
                    else:
                        break
                path_elements = path_elements[:index-1] + path_elements[index+1:]
            except ValueError:
                break
        return GitWikiUrl(self.is_absolute, path_elements)


class PathManager:
    """
    PathManager is responsible for managing paths in gitwiki

    """
    def __init__(self, templates_base_path, base_path):
        """
        Creates a PathManager instance

        :param templates_base_path: The parent of the gitwiki templates repository where the templates folder is located
        :param base_path: The root of the wiki repository, where the pages and other assets are stored
        """
        self.templates_path = join(templates_base_path, 'templates')
        loader = PackageLoader("gitwiki", "templates")
        self.jinja_env = Environment(
            loader=loader,
        )
        self.base_path = base_path
        self.base_pathlib_path = Path(base_path)

    def get_templates_path(self):
        return self.templates_path

    def get_jinja_template(self, template_name):
        return self.jinja_env.get_template(template_name)

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


    # TODO implement
    def _contains_index(self, path: str) -> bool:
        return self._exists_on_disk(join(path, INDEX_FILE_NAME))

    def _exists_on_disk(self, path: str) -> bool:
        # TODO already includes base_path ?
        return exists(join(self.base_path, path))

    def get_path_info_from_url(self, raw_url_path: str) -> PathInfo:
        # TODO portability because of separator
        # TODO handle .md files extensions
        # TODO handle folders which should default to index.md
        # TODO Create object to handle this stuff and make it testable

        decoded_url_path = parse.unquote(raw_url_path)
        raw_path_elts = decoded_url_path.split(URL_CHARACTER_SEPARATOR)

        unslashed_decoded_url_path = decoded_url_path
        cleaned_path_elts = raw_path_elts

        # if url starts with splash, remove it
        if raw_path_elts[0] == '':
            unslashed_decoded_url_path = decoded_url_path[1:]
            cleaned_path_elts = raw_path_elts[1:]

        # test is true if last char is '/' and then split returns empty
        # string at the end
        if raw_path_elts[-1] == '':
            # Folder case
            path_nature = None
            if self._exists_on_disk(unslashed_decoded_url_path):
                if self._contains_index(unslashed_decoded_url_path):
                    path_nature = PathNature.folder_with_index
                else:
                    path_nature = PathNature.folder_without_index
            else:
                path_nature = PathNature.not_found
            return PathInfo(path_nature=path_nature,
                            path_on_disk=join(self.base_path, unslashed_decoded_url_path, INDEX_FILE_NAME),
                            url_items=cleaned_path_elts)

        # File case : look for extension
        last_elt = raw_path_elts[-1]
        file_parent_url_items = cleaned_path_elts[:-1]
        file_elts = last_elt.split('.')
        extension = file_elts[-1]
        if len(file_elts) == 1:
            # No extension
            path_nature = None
            potential_md_path = join(self.base_path, unslashed_decoded_url_path + '.md')
            if self._exists_on_disk(potential_md_path):
                return PathInfo(path_nature=PathNature.md_file,
                                path_on_disk=potential_md_path,
                                url_items=cleaned_path_elts)
            else:
                return PathInfo(path_nature=PathNature.not_found,
                                path_on_disk=None,
                                url_items=cleaned_path_elts)
        else:
            if self._exists_on_disk(unslashed_decoded_url_path):
                return PathInfo(path_nature=PathNature.other_resource_file,
                                path_on_disk=join(self.base_path, decoded_url_path),
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
