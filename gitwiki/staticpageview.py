from flask.views import View
from flask import render_template
from flask import Response
from flask import send_from_directory


class StaticView(View):
    def __init__(self, path_manager):
        self.path_manager = path_manager

    def dispatch_request(self, path):
        print('Static Path %s' % path)
        return send_from_directory('templates', path, as_attachment=False)
