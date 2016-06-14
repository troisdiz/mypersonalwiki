from os.path import join
from urllib import parse

INDEX_FILE_NAME = 'index.md'
URL_CHARACTER_SEPARATOR = '/'


class PathManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_path_from_url(self, raw_url_path):
        # TODO portability because of separator
        # TODO handle .md files extensions
        # TODO handle folders which should default to index.md
        # TODO Create object to handle this stuff and make it testable

        decoded_url_path = parse.unquote(raw_url_path)
        path_elts = decoded_url_path.split(URL_CHARACTER_SEPARATOR)
        if path_elts[-1] == '':
            # Folder case
            return join(self.base_path, decoded_url_path, INDEX_FILE_NAME)

        # look for extension
        last_elt = path_elts[-1]
        file_elts = last_elt.split('.')
        extension = file_elts[-1]
        if len(file_elts) == 1:
            if extension != '':
                return join(self.base_path, decoded_url_path + '.md')
            else:
                print("Error !")
        else:
            return join(self.base_path, decoded_url_path)

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
