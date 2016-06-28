# flake8: noqa
from flask import Flask
from flask_assets import Environment, Bundle

app = Flask(__name__)

# Flask Assets
assets = Environment(app)
css = Bundle('css/custom.css', filters='cssmin', output='css/custom.min.css')
js = Bundle('js/map.js', filters='jsmin', output='js/map.min.js')
assets.register('custom_css', css)
assets.register('map_js', js)

app.config.from_pyfile('config.py')

import application.views
