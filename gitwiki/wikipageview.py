from flask.views import View
from flask import render_template


class WikiView(View):
    def __init__(self, path_manager, page_renderer, path_renderer):
        self.path_manager = path_manager
        self.page_renderer = page_renderer
        self.path_renderer = path_renderer

    def dispatch_request(self, path):
        print('Path %s' % path)

        page_path = self.path_manager.get_path_from_url(path)

        path_list = path.split('/')

        html_content = self.page_renderer.render_page(page_path)
        breadcrumb_content = self.path_renderer.render_path(path_list)
        toc_content = "Table of Content"
        sidebar_content = "Sidebar Content"
        return render_template('index.html',
                               content=html_content,
                               sidebar="Sidebar Content",
                               table_of_content="Table of content",
                               breadcrumb=breadcrumb_content)
