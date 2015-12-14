import json
import requests
from application import app
from application.utils import get_mp_data
from flask import render_template

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/petitions', methods=["GET"])
def petitions():
    url = 'https://petition.parliament.uk/petitions.json'
    r = requests.get(url)
    data = json.loads(r.text)
    return render_template('petitions.html', data=data)

@app.route('/petitions/<id>', methods=["GET"])
def petition(id):
    url = 'https://petition.parliament.uk/petitions/' + id + '.json'
    r = requests.get(url)
    data = json.loads(r.text)
    return render_template('petition.html', data=data)
