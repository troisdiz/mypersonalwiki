from sys import prefix

from gitwiki.pathmanager import PathInfo, PathManager


class SidebarRenderer:

    def __init__(self, base_url: str, path_manager: PathManager) -> None:
        self.base_url = base_url
        self.path_manager = path_manager

    def render_sidebar(self, elements:  list[tuple[PathInfo, bool]]) -> str:

        sidebar_content = "<ul>\n"
        for element in elements:
            url_relative_path: str = self.path_manager.url_from_path(element[0])
            title = self.path_manager.title_from_path(element[0])
            if element[0].is_folder():
                prefix = "<i class=\"bi bi-folder\">TOTO</i>"
            else:
                prefix = "P - "

            if element[1]:
                rendered_title = f"<span style=\"font-weight: bold;\">{prefix}Current</span>"
            else:
                rendered_title = title
            sidebar_content += f"<li><a class=\"wikilink\" href=\"{url_relative_path}\">{prefix}{rendered_title}</a></li>\n"
        sidebar_content += "</ul>\n"
        print(f"Found {len(elements)} siblings")
        for child in elements:
            print(f"    Found child : {child}")
        print()
        sidebar_content += "\n<ul>\n"
        return sidebar_content
