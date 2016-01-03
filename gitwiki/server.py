import markdown
import codecs
import os.path
from markdown.extensions.wikilinks import WikiLinkExtension
from flask import Flask, render_template
import sys
from gitwiki.pathmanager import PathManager


base_pages_path = "/tmp"
path_manager = None

app = Flask(__name__)


@app.route('/')
def hello_world():
    input_file = codecs.open("index.md", mode="r", encoding="utf-8")
    text = input_file.read()

    html = markdown.markdown(text, extensions=['markdown.extensions.codehilite',
                                               'markdown.extensions.toc',
                                               WikiLinkExtension(base_url='/pages/', end_url='.md')])

    output_file = codecs.open("output.html", "w",
                              encoding="utf-8",
                              errors="xmlcharrefreplace")
    output_file.write(html)

    return 'Hello World!'


@app.route('/pages/<path:path>')
def show_user_profile(path):
    print('Path %s' % path)

    page_path = get_path_from_url(path)

    input_file = codecs.open(page_path, mode="r", encoding="utf-8")
    text = input_file.read()
    html_content = markdown.markdown(text, extensions=['markdown.extensions.codehilite',
                                                       'markdown.extensions.toc',
                                                       WikiLinkExtension(base_url='/pages/', end_url='.md')])
    html_path = '<div class=\'breadcrumb\'>path 1</div>'
    return render_template('base.html',
                           content=html_content,
                           path=html_path)


def get_path_from_url(url):
    return path_manager.get_path_from_url(url)


if __name__ == "__main__":
    base_pages_path = sys.argv[1]
    path_manager = PathManager(base_pages_path)
    print("Base page path = %s" % base_pages_path)
    app.run(host='0.0.0.0', port=8080, debug=True)
