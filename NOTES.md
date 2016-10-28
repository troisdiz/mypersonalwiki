# Dev Setup #

1. Setup python

    virtualenv venv
    ./venv/bin/activate
    pip install -r requirements.txt

1. Setup Web
    
    cd static
    npm install
    npm install -g bower
    bower install
    npm install -g grunt
    grunt build

1. Finish python setup

    (from static)
    rm -rf ../gitwiki/templates/* && cp -r dist/* ../gitwiki/templates/. 
   
1. run server
    
    (From gitwiki)
    export PYTHONPATH=$PYTHONPATH:`pwd`
    python gitwiki/server.py [Pages root path]
    
   
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

## Web ##

* [[http://getbootstrap.com/components/#panels]]
* [[http://sass-lang.com/guide]]
* [[http://startbootstrap.com/template-overviews/sb-admin-2/]]
* [[http://blackrockdigital.github.io/startbootstrap-sb-admin-2/pages/index.html]]
