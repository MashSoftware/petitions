import json
import requests
from application import app
from application.utils import get_mp, constituency_extent, constituency_collection, petition_events, petition_deadline
from flask import render_template, request
from operator import itemgetter

@app.route('/', methods=["GET"])
def index():
    title='Home'
    return render_template('index.html', title=title)

@app.route('/petitions', methods=["GET"])
def petitions():
    title='Petitions'
    args = request.args.items()
    url = 'https://petition.parliament.uk/petitions.json?' + ''.join("%s=%s&" % tup for tup in args)
    page = request.args.get('page')
    r = requests.get(url)
    data = json.loads(r.text)
    return render_template('petitions.html', title=title, data=data, page=page, args=args)

@app.route('/petitions/<id>', methods=["GET"])
def petition(id):
    url = 'https://petition.parliament.uk/petitions/' + id + '.json'
    r = requests.get(url)
    data = json.loads(r.text)

    title = data['data']['attributes']['action']

    countries = data['data']['attributes']['signatures_by_country']
    sorted_countries = sorted(countries, key=itemgetter('signature_count'), reverse=True)

    constituencies = data['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    for constituency in sorted_constituencies [:10]:
        mp = get_mp(constituency['name'])
        constituency['party'] = mp['party']
        constituency['url'] = mp['url']
        if 'image' in mp:
            constituency['mp_image'] = mp['image']

    extents = constituency_collection(sorted_constituencies)

    events = petition_events(data)
    deadline = petition_deadline(data)

    return render_template('petition.html',
        title=title,
        data=data,
        countries=sorted_countries,
        constituencies=sorted_constituencies,
        extents=extents,
        events=events)

@app.route('/petitions/<id>/map', methods=["GET"])
def map(id):
    url = 'https://petition.parliament.uk/petitions/' + id + '.json'
    r = requests.get(url)
    data = json.loads(r.text)

    title = data['data']['attributes']['action']

    constituencies = data['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    for constituency in sorted_constituencies [:10]:
        mp = get_mp(constituency['name'])
        constituency['party'] = mp['party']
        constituency['url'] = mp['url']

    extents = constituency_collection(sorted_constituencies)

    return render_template('map.html',
        title=title,
        extents=extents)

@app.route('/petitions/<id>/history', methods=["GET"])
def history(id):
    url = 'https://petition.parliament.uk/petitions/' + id + '.json'
    r = requests.get(url)
    data = json.loads(r.text)

    title = data['data']['attributes']['action']
    events = petition_events(data)
    deadline = petition_deadline(data)

    return render_template('history.html', title=title, data=data, events=events)
