from flask.views import View
from flask import Flask, render_template
import codecs
from markdown.extensions.wikilinks import WikiLinkExtension
import markdown


class WikiView(View):
    def __init__(self, path_manager):
        self.path_manager = path_manager

    def dispatch_request(self, path):
        print('Path %s' % path)

        page_path = self.path_manager.get_path_from_url(path)

        input_file = codecs.open(page_path, mode="r", encoding="utf-8")
        text = input_file.read()
        html_content = markdown.markdown(text, extensions=['markdown.extensions.codehilite',
                                                           'markdown.extensions.toc',
                                                           WikiLinkExtension(base_url='/pages/', end_url='.md')])
        html_path = '<div class=\'breadcrumb\'>path 1</div>'
        return render_template('base.html',
                               content=html_content,
                               path=html_path)
