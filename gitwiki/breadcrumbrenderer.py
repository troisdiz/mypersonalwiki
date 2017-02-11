from jinja2 import Template
from gitwiki.extensions.gitwikilinks import build_url_from_paths

BREADCRUMB_ITEM = """<li{%if class_attr is defined %}class="{{class_attr}}"{% endif %}>{% if link is defined %}
    <a href="{{link}}">{{text}}</a>{% else %}
    {{text}}
    {% endif %}
</li>"""


class BreadcrumbRender:
    def __init__(self, base_url):
        self.base_url = base_url
        self.template = Template(BREADCRUMB_ITEM, trim_blocks=True, lstrip_blocks=False)

    def render_path(self, path_list):
        if path_list is not None:

            result = [self.template.render(link=build_url_from_paths(path_item[0],
                                                                     self.base_url,
                                                                     True),
                                           text=path_item[1])
                      for path_item in build_tuples(path_list)]
            return "\n".join(result)
        else:
            return ''


def build_tuples(path_list):
    current_path = []
    yield (current_path, 'Home')
    for path_item in path_list:
        current_path = list(current_path + [path_item])
        yield (current_path, path_item)
