import json
import requests
from application import app
from application.utils import get_mp, constituency_extent, constituency_collection, petition_events
from flask import render_template, request
from operator import itemgetter

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/petitions', methods=["GET"])
def petitions():
    args = request.args.items()
    url = 'https://petition.parliament.uk/petitions.json?' + ''.join("%s=%s&" % tup for tup in args)
    page = request.args.get('page')
    r = requests.get(url)
    data = json.loads(r.text)
    return render_template('petitions.html', data=data, page=page, args=args)

@app.route('/petitions/<id>', methods=["GET"])
def petition(id):
    url = 'https://petition.parliament.uk/petitions/' + id + '.json'
    r = requests.get(url)
    data = json.loads(r.text)

    countries = data['data']['attributes']['signatures_by_country']
    sorted_countries = sorted(countries, key=itemgetter('signature_count'), reverse=True)

    constituencies = data['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    # for constituency in sorted_constituencies [:10]:
    #     mp = get_mp(constituency['name'])
    #     constituency['party'] = mp['party']
    #     constituency['url'] = mp['url']
    #     if 'image' in mp:
    #         constituency['mp_image'] = mp['image']

    extents = constituency_collection(sorted_constituencies)

    events = petition_events(data)

    return render_template('petition.html',
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

    constituencies = data['data']['attributes']['signatures_by_constituency']
    sorted_constituencies = sorted(constituencies, key=itemgetter('signature_count'), reverse=True)

    for constituency in sorted_constituencies [:10]:
        mp = get_mp(constituency['name'])
        constituency['party'] = mp['party']
        constituency['url'] = mp['url']

    extents = constituency_collection(sorted_constituencies)

    return render_template('map.html',
        extents=extents)
