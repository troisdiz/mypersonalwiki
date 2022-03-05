from flask.views import View
from flask import render_template, abort, send_file
from gitwiki.pathmanager import PathNature


class WikiView(View):
    def __init__(self, path_manager, page_renderer, breadcrumb_renderer):
        self.path_manager = path_manager
        self.page_renderer = page_renderer
        self.breadcrumb_renderer = breadcrumb_renderer

    def dispatch_request(self, path):

        path_info = self.path_manager.get_path_info_from_url(path)

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
        elif (path_info.pathNature == PathNature.folder_with_index) | (path_info.pathNature == PathNature.md_file):
            return self.return_wiki_page(path_info.path_on_disk, path_info.url_items)
        elif path_info.pathNature == PathNature.folder_without_index:
            print('PathNature folder without index : TODO 3')

    def return_wiki_page(self, page_path_on_disk, path_elements):

        print(f"Wiki page view : path_elements={path_elements}")

        toc_content, html_content = self.page_renderer.render_page(page_path_on_disk)
        breadcrumb_content = self.breadcrumb_renderer.render_path(path_elements)
        relative_to_root = ".."
        for i in range(len(path_elements)):
            relative_to_root = relative_to_root + "/.."
        sidebar_content = "Sidebar Content"
        return render_template('index.html',
                               relative_to_root=relative_to_root,
                               content=html_content,
                               sidebar=sidebar_content,
                               table_of_content=toc_content,
                               breadcrumb=breadcrumb_content)
