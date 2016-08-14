from jinja2 import Template
from gitwiki.extensions.gitwikilinks import build_url_from_paths

BREADCRUMB_ITEM = """<li {%if class_attr is defined %}class="{{class_attr}}"{% endif %}>{% if link is defined %}
    <a href="{{link}}">{{text}}</a>{% else %}
    {{text}}
    {% endif %}
</li>"""


class BreacrumbRender:
    def __init__(self, base_url):
        self.base_url = base_url
        self.template = Template(BREADCRUMB_ITEM, trim_blocks=True, lstrip_blocks=False)

    def render_path(self, path_list):
        result = [self.template.render(link=build_url_from_paths(path_item[0],
                                                                 '/pages/',
                                                                 '.md'),
                                       text=path_item[1])
                  for path_item in self.build_tuples(path_list)]
        return "\n".join(result)

    def build_tuples(self, path_list):
        current_path = []
        yield (current_path, 'Home')
        for path_item in path_list:
            current_path = current_path + [path_item]
            yield (current_path, path_item)
