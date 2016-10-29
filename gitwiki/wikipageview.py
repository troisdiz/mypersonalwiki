from flask.views import View
from flask import render_template, abort, send_file
from gitwiki.pathmanager import PathNature


class WikiView(View):
    def __init__(self, path_manager, page_renderer, breadcrumb_renderer):
        self.path_manager = path_manager
        self.page_renderer = page_renderer
        self.breadcrumb_renderer = breadcrumb_renderer

    def dispatch_request(self, path):
        print('Path %s' % path)

        path_info = self.path_manager.get_path_info_from_url(path)

        print('Path (url)  = ' + path)
        print('PathNature  = ' + str(path_info.pathNature))
        print('path (disk) = ' + path_info.path_on_disk)

        if path_info.pathNature == PathNature.not_found:
            # TODO customize page (give path ?)
            abort(404)
        elif path_info.pathNature == PathNature.other_resource_not_found:
            abort(404)
        elif path_info.pathNature == PathNature.other_resource_file:
            # TODO mime type
            return send_file(path_info.path_on_disk, mimetype='image/png')
        elif (path_info.pathNature == PathNature.folder_with_index) | (path_info.pathNature == PathNature.md_file):
            return self.return_wiki_page(path_info.path_on_disk, path_info.url_items)
        elif path_info.pathNature == PathNature.folder_without_index:
            print('TODO 2')

    def return_wiki_page(self, page_path_on_disk, path_elements):

        html_content = self.page_renderer.render_page(page_path_on_disk)
        breadcrumb_content = self.breadcrumb_renderer.render_path(path_elements)
        toc_content = "Table of Content"
        sidebar_content = "Sidebar Content"
        return render_template('index.html',
                               content=html_content,
                               sidebar="Sidebar Content",
                               table_of_content="Table of content",
                               breadcrumb=breadcrumb_content)
