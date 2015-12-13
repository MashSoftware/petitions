import json
import requests

from application import app
from flask import render_template

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/petition', methods=["GET"])
def petition():
    url = 'https://petition.parliament.uk/petitions/114003.json'
    r = requests.get(url)

    data = json.loads(r.text)

    return render_template('petition.html', data=data)
