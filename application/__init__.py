# flake8: noqa
from flask import Flask
app = Flask(__name__)

app.config.from_pyfile('config.py')

import application.views
