# Dev Setup #

1. Setup python

    python3 -m venv venv
    ./venv/bin/activate
    pip install -r requirements.txt

1. Generate Pygments CSS

```bash
# Needs virtualenv to be activated
# To be ran project root
pygmentize -S default -f html > static/app/styles/pygments.css
```

1. Setup Web

1. Finish python setup

```bash
# From root
cp -r static/app/* src/gitwiki/templates/.
```

1. run server

```bash
# From project root
export PYTHONPATH=$PYTHONPATH:`pwd`
python gitwiki/server.py [Pages root path]
```

# Python #

* add (almost) all markdown plugins
* Handle indexes

# HTML #

* Bootstrap layout
* add codehilite css

# Other #

* Git

# Links #

## Python ##

* [[https://www.browsersync.io/]]
* [[https://pythonhosted.org/Markdown/]]
* [[http://mozilla.github.io/nunjucks/]]
* [[https://help.github.com/articles/markdown-basics/]]
* [[https://guides.github.com/features/mastering-markdown/]]
* [[https://help.github.com/articles/github-flavored-markdown/]]
* [[http://getbootstrap.com/getting-started/]]
* [[http://daringfireball.net/projects/markdown/syntax]]
* [[http://pygments.org/]]
* [[https://pythonhosted.org/Markdown/reference.html]]
* [[https://pythonhosted.org/Markdown/extensions/index.html]]
* [[https://docs.python.org/3.4/library/os.html]]
* [[https://docs.python.org/3/library/os.path.html]]
* [[https://github.com/FND/markdown-checklist]]
* [[https://github.com/smartboyathome/Markdown-GridTables/]]
* [[https://pythonhosted.org/Flask-Markdown/]]
* [[https://pythonhosted.org/Markdown/extensions/api.html]]
* [[https://pythonhosted.org/Markdown/extensions/smarty.html]]
* [[https://github.com/waylan/Python-Markdown/wiki/Third-Party-Extensions]]

## Web ##

* [[http://getbootstrap.com/components/#panels]]
* [[http://sass-lang.com/guide]]
* [[http://startbootstrap.com/template-overviews/sb-admin-2/]]
* [[http://blackrockdigital.github.io/startbootstrap-sb-admin-2/pages/index.html]]
