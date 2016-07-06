# flake8: noqa
from flask import Flask
from flask_compress import Compress
from flask_cache import Cache
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#App config
app.config.from_pyfile('config.py')

# Flask Compress
Compress(app)

# Flask Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

#SQL Alchemy
db = SQLAlchemy(app)

import application.views
import application.models
