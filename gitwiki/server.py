from flask import Flask, render_template
import sys
from .pathmanager import PathManager
from .wikipageview import WikiView

if __name__ == "__main__":
    base_pages_path = sys.argv[1]
    path_manager = PathManager(base_pages_path)
    print("Base page path = %s" % base_pages_path)

    app = Flask('Personal Wiki')
    wiki_page_view = WikiView.as_view(name='wiki_page_view', path_manager=path_manager)
    app.add_url_rule(rule='/pages/<path:path>', view_func=wiki_page_view)

    app.run(host='0.0.0.0', port=8080, debug=True)
