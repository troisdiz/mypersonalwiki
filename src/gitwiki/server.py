import flask
from flask import Flask, redirect
from jinja2 import PackageLoader
import sys
import os
from gitwiki.pathmanager import PathManager
from gitwiki.pagerenderer import PageRenderer
from gitwiki.breadcrumbrenderer import BreadcrumbRenderer
from gitwiki.wikipageview import WikiView
from gitwiki.staticpageview import StaticView

BASE_PAGE_URL = '/pages/'


def create_flask_app(base_pages_path: str) -> flask.Flask:
    program_base_path = os.path.dirname(os.path.realpath(__file__))

    path_manager = PathManager(program_base_path, base_pages_path)
    page_renderer = PageRenderer(base_url=BASE_PAGE_URL, base_pages_path=base_pages_path)
    breadcrumb_renderer = BreadcrumbRenderer(BASE_PAGE_URL)
    print("Base page path = %s" % base_pages_path)

    app = Flask('Personal Wiki')
    wiki_page_view = WikiView.as_view(name='wiki_page_view',
                                      path_manager=path_manager,
                                      page_renderer=page_renderer,
                                      breadcrumb_renderer=breadcrumb_renderer)
    static_page_view = StaticView.as_view(name='static_page_view',
                                          path_manager=path_manager)
    app.add_url_rule(rule=BASE_PAGE_URL, view_func=wiki_page_view, defaults={'path': ''})
    app.add_url_rule(rule=BASE_PAGE_URL + '<path:path>', view_func=wiki_page_view)
    app.add_url_rule(rule='/_mpw_static/<path:path>', view_func=static_page_view)

    @app.route('/')
    def index():
        return redirect(BASE_PAGE_URL)

    return app


if __name__ == "__main__":
    base_pages_path = sys.argv[1]
    app = create_flask_app(base_pages_path)

    # Try to use a port for debug with minimal collisions
    app.run(host='127.0.0.1', port=8085, debug=True)
