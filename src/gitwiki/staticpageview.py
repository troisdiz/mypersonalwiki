from flask.views import View
from flask import render_template
from flask import Response
from flask import send_from_directory

from gitwiki.pathmanager import PathManager


class StaticView(View):
    """
    Flask View to serve static files which are part of gitwiki (not the statics assets of the wiki)

    Examples are the css, the js to do the rendering of the wiki pages.
    """

    def __init__(self, path_manager):
        self.path_manager: PathManager = path_manager

    def dispatch_request(self, path):
        print('Serve static Path %s' % path)
        return send_from_directory(self.path_manager.get_templates_path(), path, as_attachment=False)
