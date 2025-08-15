# GitWiki

This is a personal project aiming at creating a simple wiki system based on git and markdown.
It can be used to create a personal wiki and be hosted on multiple machines (the initial goal is to
run it on a laptop) and doing synchronization between them using git.

## Development Setup

The front code is in the `static` folder and is implemented using Bootstrap and packaged using Webpack.
The backend code is in the `src` folder and is implemented in Python using Flask and Markdown.
Here are the steps to setup the development environment:

1. Setup Python

```bash
    # Assummes the expected Python3 is in your PATH, you can use another python3
    # Development is done using Python 3.13.5 (lastest at the time of writing) but should be compatible with lower versions.
    python3 -m venv venv
    ./venv/bin/activate
    pip install -r requirements.txt
```

1. Generate Pygments CSS

```bash
# Needs virtualenv to be activated
# To be ran in project root
pygmentize -S default -f html > static/src/pygments.css

# For later
# .syntax of the CSS selector of the parent element
# To be used in the python code
# pygmentize -S default -f html -a .syntax> static/app/styles/pygments.css
```

1. Setup Front

```bash
    # From static folder
    # Assumes you have Node.js and yarn2 installed (I use https://volta.sh/)
    yarn install
    # Depending on what you want to do, you can use one of the following commands:
    yarn build # For production build and backend development
    # OR
    yarn build-dev # For Front development
```

1. Run Python server

  1.1. Debug mode
```bash
    # From src folder
    # Assumes you have the virtualenv activated
    export PYTHONPATH=$PYTHONPATH:`pwd`
    python gitwiki/server.py [Pages root path]
```

  1.2. Granian mode

```bash
    # From project root folder
    # Does NOT assume you have the virtualenv activated
    ./start_granian.sh [Pages root path]
```

## Main opensource projects used

* Python
  * [Python-Markdown](https://python-markdown.github.io/)
    * [Markdown syntax guide](https://www.markdownguide.org/basic-syntax/)
  * [Flask](https://flask.palletsprojects.com/en/stable/)
  * [Pygments](http://pygments.org/)
* Bootstrap
* Webpack

## Further development ideas

* add (almost) all Python Markdown plugins
* add a Mermaid plugin
* add a MathJax plugin
* Add the concept of page title (to be used in the HTML title tag and at the top of the page)
  * Handle indexes (needs the previous one)
  * Handle subpages view (needs the previous one)
* Git
  * Display git information (last commit, author, date, etc.)
  * Display git history (diagram?)

## Links

Needs to be updated/triaged

* [[https://help.github.com/articles/markdown-basics/]]
* [[https://guides.github.com/features/mastering-markdown/]]
* [[https://help.github.com/articles/github-flavored-markdown/]]
* [[http://getbootstrap.com/getting-started/]]
* [[http://daringfireball.net/projects/markdown/syntax]]
* [[https://github.com/FND/markdown-checklist]]
* [[https://github.com/smartboyathome/Markdown-GridTables/]]
* [[https://github.com/waylan/Python-Markdown/wiki/Third-Party-Extensions]]
* [[http://getbootstrap.com/components/#panels]]
* [[http://sass-lang.com/guide]]
* [[http://startbootstrap.com/template-overviews/sb-admin-2/]]
* [[http://blackrockdigital.github.io/startbootstrap-sb-admin-2/pages/index.html]]
