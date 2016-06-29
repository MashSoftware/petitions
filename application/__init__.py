# flake8: noqa
from flask import Flask
from flask_assets import Environment, Bundle
from flask_compress import Compress

app = Flask(__name__)

#App config
app.config.from_pyfile('config.py')

# Flask Assets
assets = Environment(app)
css = Bundle('css/custom.css', filters='cssmin', output='css/custom.min.css')
js = Bundle('js/map.js', filters='jsmin', output='js/map.min.js')
assets.register('custom_css', css)
assets.register('map_js', js)

# Flask Compress
Compress(app)

import application.views
