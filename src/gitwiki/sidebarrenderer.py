from gitwiki.pathmanager import PathInfo, PathManager


class SidebarRenderer:

    def __init__(self, base_url: str, path_manager: PathManager) -> None:
        self.base_url = base_url
        self.path_manager = path_manager

    def render_sidebar(self, elements: list[PathInfo]) -> str:

        sidebar_content = "<ul>\n"
        for element in elements:
            url_relative_path: str = self.path_manager.url_from_path(element)
            sidebar_content += f"<li>{url_relative_path}</li>\n"
        sidebar_content += "</ul>\n"
        print(f"Found {len(elements)} siblings")
        for child in elements:
            print(f"    Found child : {child}")
        print()
        sidebar_content += "\n<ul>\n"
        for child in elements:
            sidebar_content += f"    <li>{child.name()}</li>\n"

        sidebar_content += "</ul>\n"
        return sidebar_content
