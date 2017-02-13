#!/usr/bin/env bash

pip install -r requirements.txt
pygmentize -S default -f html > static/app/styles/pygments.css

cd static
npm install
npm install -g bower
bower install
npm install -g grunt
grunt build
cd ..

rm -rf gitwiki/templates/* && cp -r static/dist/* gitwiki/templates/.
