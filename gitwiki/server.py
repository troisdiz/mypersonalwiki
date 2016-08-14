from flask import Flask
import sys
import os
from gitwiki.pathmanager import PathManager
from gitwiki.pagerenderer import PageRenderer
from gitwiki.breadcrumbrenderer import BreacrumbRender
from gitwiki.wikipageview import WikiView
from gitwiki.staticpageview import StaticView

if __name__ == "__main__":
    base_pages_path = sys.argv[1]
    program_base_path = os.path.dirname(os.path.realpath(__file__))

    path_manager = PathManager(base_pages_path)
    page_renderer = PageRenderer(base_pages_path)
    path_renderer = BreacrumbRender('/pages')
    print("Base page path = %s" % base_pages_path)

    app = Flask('Personal Wiki')
    wiki_page_view = WikiView.as_view(name='wiki_page_view',
                                      path_manager=path_manager,
                                      page_renderer=page_renderer,
                                      path_renderer=path_renderer)
    static_page_view = StaticView.as_view(name='static_page_view',
                                          path_manager=path_manager)
    app.add_url_rule(rule='/pages/<path:path>', view_func=wiki_page_view)
    app.add_url_rule(rule='/static2/<path:path>', view_func=static_page_view)

    app.run(host='0.0.0.0', port=8080, debug=True)
    app.make_response("toto")
