from flask.views import View


class WikiView(View):
    def __init__(self, path_manager, page_renderer):
        self.path_manager = path_manager
        self.page_renderer = page_renderer

    def dispatch_request(self, path):
        print('Path %s' % path)

        page_path = self.path_manager.get_path_from_url(path)

        return self.page_renderer.render_page(page_path)
