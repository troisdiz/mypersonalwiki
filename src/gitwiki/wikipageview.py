from pathlib import Path

from string import Template

from flask.views import View
from flask import render_template, abort, send_file

from gitwiki.breadcrumbrenderer import BreadcrumbRenderer
from gitwiki.pagerenderer import PageRenderer
from gitwiki.pathmanager import PathInfo, PathNature, PathManager, TemplateManager, INDEX_FILE_NAME
from gitwiki.sidebarrenderer import SidebarRenderer


class WikiView(View):
    def __init__(self,
                 path_manager: PathManager,
                 template_manager: TemplateManager,
                 page_renderer: PageRenderer,
                 breadcrumb_renderer: BreadcrumbRenderer,
                 sidebar_renderer: SidebarRenderer):
        self.path_manager: PathManager = path_manager
        self.template_manager: TemplateManager = template_manager
        self.page_renderer: PageRenderer = page_renderer
        self.breadcrumb_renderer: BreadcrumbRenderer = breadcrumb_renderer
        self.sidebar_renderer: SidebarRenderer = sidebar_renderer

        self.index_template = self.template_manager.get_jinja_template('index.html')

    def dispatch_request(self, path):

        path_info: PathInfo = self.path_manager.get_path_info_from_url(path)

        print('Path (url)  = ' + path)
        print('PathInfo  = ' + str(path_info))

        if path_info.pathNature == PathNature.not_found:
            # TODO customize page (give path ?)
            print('PathNature not found -> 404')
            abort(404)
        elif path_info.pathNature == PathNature.other_resource_not_found:
            print('PathNature other resource not found -> 404')
            abort(404)
        elif path_info.pathNature == PathNature.other_resource_file:
            # TODO mime type
            return send_file(path_info.path_on_disk, mimetype='image/png')
        elif (path_info.pathNature == PathNature.folder_with_index) | \
                (path_info.pathNature == PathNature.folder_without_index) | \
                (path_info.pathNature == PathNature.md_file):
            return self.return_wiki_page(path_info, Path(path_info.path_on_disk), path_info.url_items)
        elif path_info.pathNature == PathNature.folder_without_index:
            print('PathNature folder without index : TODO 3')
            abort(500)
        else:
            print('PathNature default case -> 500')
            abort(500)

    def return_wiki_page(self, path_info: PathInfo, page_path_on_disk: Path, path_elements: list[str]) -> str:

        print("Enter return_wiki_page")
        print(f"    path_info = {path_info}")
        print(f"    page_path_on_disk = {page_path_on_disk}")
        print(f"    path_elements={path_elements}")

        toc_content, html_content = None, None
        match path_info.pathNature:
            case PathNature.folder_without_index:
                toc_content, html_content = self.page_renderer.render_folder_without_index(path_on_disk=page_path_on_disk)
            case PathNature.folder_with_index:
                toc_content, html_content = self.page_renderer.render_page(path_on_disk=page_path_on_disk / "index.md")
            case PathNature.md_file:
                toc_content, html_content = self.page_renderer.render_page(path_on_disk=page_path_on_disk)

        breadcrumb_content = self.breadcrumb_renderer.render_path(path_elements)
        relative_to_root = ".."
        for i in range(len(path_elements)):
            relative_to_root = relative_to_root + "/.."
        children: list[PathInfo] = self.path_manager.get_sibling_paths(path_info)


        sidebar_content = self.sidebar_renderer.render_sidebar(children)

        print(f"    Sidebar Content:\n{sidebar_content}")
        return render_template(self.index_template,
                               relative_to_root=relative_to_root,
                               content=html_content,
                               sidebar=sidebar_content,
                               table_of_content=toc_content,
                               breadcrumb=breadcrumb_content)
