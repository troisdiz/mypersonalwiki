from os.path import join
from os.path import exists
from urllib import parse
from enum import Enum
from enum import unique

INDEX_FILE_NAME = 'index.md'
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
    def __init__(self, path_nature, path_on_disk, url_items=None):
        self.pathNature = path_nature
        self.path_on_disk = path_on_disk
        # TODO
        if url_items is None:
            self.url_items = []
        else:
            self.url_items = url_items


class MalFormedGitWikiUrl(Exception):

    def __init__(self, message):
        self.message = message


class GitWikiUrl:
    # 2 subslasses (abs and rel ?)
    def __init__(self, is_absolute, path_elements):
        self.is_absolute = is_absolute
        self.path_elements = path_elements

    def canonize(self):
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
    def __init__(self, base_path):
        self.base_path = base_path

    # TODO implement
    def contains_index(self, path):
        return self.exists_on_disk(join(path, INDEX_FILE_NAME))

    def exists_on_disk(self, path):
        # TODO already includes base_path ?
        return exists(join(self.base_path, path))

    def get_path_info_from_url(self, raw_url_path):
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
            if self.exists_on_disk(unslashed_decoded_url_path):
                if self.contains_index(unslashed_decoded_url_path):
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
            if self.exists_on_disk(potential_md_path):
                return PathInfo(path_nature=PathNature.md_file,
                                path_on_disk=potential_md_path,
                                url_items=file_parent_url_items)
            else:
                return PathInfo(path_nature=PathNature.not_found,
                                path_on_disk=None,
                                url_items=file_parent_url_items)
        else:
            if self.exists_on_disk(unslashed_decoded_url_path):
                return PathInfo(path_nature=PathNature.other_resource_file,
                                path_on_disk=join(self.base_path, decoded_url_path),
                                url_items=file_parent_url_items)
            else:
                return PathInfo(path_nature=PathNature.other_resource_not_found,
                                path_on_disk=None,
                                url_items=file_parent_url_items)

    def get_static_path_from_url(self, raw_url_path):
        # TODO portability because of separator
        # TODO handle .md files extensions
        # TODO handle folders which should default to index.md
        # TODO Create object to handle this stuff and make it testable

        decoded_url_path = parse.unquote(raw_url_path)
        path_elts = decoded_url_path.split(URL_CHARACTER_SEPARATOR)
        return join(self.base_path, decoded_url_path)


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
