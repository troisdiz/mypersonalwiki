from os import environ

from flask import Flask
from gitwiki.server import create_flask_app

base_pages_path = environ.get("GITWIKI_PAGES_PATH")

print(f"Base pages path = {base_pages_path}")

app: Flask = create_flask_app(base_pages_path)
