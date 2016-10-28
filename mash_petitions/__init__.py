# flake8: noqa
from flask import Flask
from flask_compress import Compress
from flask_cache import Cache

app = Flask(__name__)

#App config
app.config.from_pyfile('config.py')

# Flask Compress
Compress(app)

# Flask Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

import mash_petitions.views
