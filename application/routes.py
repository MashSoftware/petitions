import json
import requests
from application import app
from application.utils import get_mp_data, constituency_extent, constituency_collection
from flask import render_template, request
from operator import itemgetter

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/petitions', methods=["GET"])
def petitions():
    if request.args.get('page'):
        url = 'https://petition.parliament.uk/petitions.json?page=' + request.args.get('page')
    else:
        url = 'https://petition.parliament.uk/petitions.json'
    page = request.args.get('page')
    r = requests.get(url)
    data = json.loads(r.text)
    return render_template('petitions.html', data=data, page=page)

@app.route('/petitions/<id>', methods=["GET"])
def petition(id):
    url = 'https://petition.parliament.uk/petitions/' + id + '.json'
    r = requests.get(url)
    data = json.loads(r.text)

    countries = data['data']['attributes']['signatures_by_country']
    sorted_countries = sorted(countries, key=itemgetter('signature_count'), reverse=True)

    constituencies = data['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    extents = constituency_collection(sorted_constituencies)

    return render_template('petition.html',
        data=data,
        countries=sorted_countries,
        constituencies=sorted_constituencies,
        extents=extents)

@app.route('/petitions/<id>/map', methods=["GET"])
def map(id):
    url = 'https://petition.parliament.uk/petitions/' + id + '.json'
    r = requests.get(url)
    data = json.loads(r.text)

    constituencies = data['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    extents = constituency_collection(sorted_constituencies)

    return render_template('map.html',
        extents=extents)
