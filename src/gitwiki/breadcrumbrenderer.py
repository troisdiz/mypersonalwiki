from typing import Generator
from jinja2 import Template
from gitwiki.extensions.gitwikilinks import build_url_from_paths

BREADCRUMB_ITEM = """<li{%if class_attr is defined %} class="{{class_attr}}"{% endif %}>{% if link is defined %}
    <a href="{{link}}">{{text}}</a>{% else %}
    {{text}}
    {% endif %}
</li>"""


class BreadcrumbRenderer:
    def __init__(self, base_url):
        self.base_url = base_url
        self.template = Template(BREADCRUMB_ITEM, trim_blocks=True, lstrip_blocks=False)

    def render_path(self, path_list):
        if path_list is not None:

            result = [self.template.render(link=build_url_from_paths(path_item[0],
                                                                     self.base_url,
                                                                     path_item[2]),
                                           text=path_item[1],
                                           class_attr="breadcrumb-item")
                      for path_item in build_tuples(path_list)]
            return "\n".join(result)
        else:
            return ''


def build_tuples(path_list: list[str]) -> Generator:
    current_path = []
    path_list_len: int = len(path_list)
    yield current_path, 'Home', True
    for idx, path_item in enumerate(path_list):
        current_path = list(current_path + [path_item])
        # The last item is always a file, so it is not a folder
        is_folder: bool = (idx != path_list_len-1)
        yield current_path, path_item, is_folder
