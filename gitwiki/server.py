from flask import Flask
import sys
from gitwiki.pathmanager import PathManager
from gitwiki.pagerenderer import PageRenderer
from gitwiki.wikipageview import WikiView

if __name__ == "__main__":
    base_pages_path = sys.argv[1]
    path_manager = PathManager(base_pages_path)
    page_renderer = PageRenderer(base_pages_path)

    print("Base page path = %s" % base_pages_path)

    app = Flask('Personal Wiki')
    wiki_page_view = WikiView.as_view(name='wiki_page_view',
                                      path_manager=path_manager,
                                      page_renderer=page_renderer)
    app.add_url_rule(rule='/pages/<path:path>', view_func=wiki_page_view)

    app.run(host='0.0.0.0', port=8080, debug=True)
