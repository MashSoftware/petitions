import requests
import json
import geojson
from application import app
from geojson import Polygon, Feature, FeatureCollection
from operator import itemgetter
from datetime import datetime, timedelta

PETITIONS_API_URL = app.config['PETITIONS_API_URL']


def get_petitions(args):
    url = '{0}.json?{1}'
    response = requests.get(url.format(PETITIONS_API_URL, ''.join("%s=%s&" % tup for tup in args)))
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        petitions = json.loads(response.text)
    return petitions


def get_petition(id):
    url = '{0}/{1}.json'
    response = requests.get(url.format(PETITIONS_API_URL, id))
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        petition = json.loads(response.text)
    return petition


def get_mp(constituency):
    twfy_api_url = app.config['TWFY_API_URL']
    twfy_api_key = app.config['TWFY_API_KEY']
    url = '{0}/getMP?key={1}&constituency={2}&output=js'
    response = requests.get(url.format(twfy_api_url, twfy_api_key, constituency))
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        data = response.json()
    return data


def constituency_extent(ons_code):
    mapit_api_url = app.config['MAPIT_API_URL']
    url = '{0}/area/{1}.geojson'
    response = requests.get(url.format(mapit_api_url, ons_code))
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        data = response.json()
    return data


def constituency_collection(constituencies):
    features = []

    for constituency in constituencies[:10]:
        feature = Feature(geometry=Polygon(constituency_extent(constituency['ons_code'])['coordinates']))
        feature.properties['name'] = constituency['name']
        feature.properties['mp'] = constituency['mp']
        # feature.properties['party'] = constituency['party']
        # feature.properties['url'] = constituency['url']
        feature.properties['signature_count'] = constituency['signature_count']
        features.append(feature)

    feature_collection = FeatureCollection(features)

    return geojson.dumps(feature_collection)


def petition_events(petition):
    events = []
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    for k, v in petition['data']['attributes'].items():
        if '_at' in k:
            if v is not None:
                event = {}
                event['datetime'] = v
                event['type'] = k.split("_at")[0]
                events.append(event)

    sorted_events = sorted(events, key=itemgetter('datetime'))
    for index, event in enumerate(sorted_events):
        event['date'] = datetime.strptime(event['datetime'], date_format).strftime("%d %B %Y")
        event['time'] = datetime.strptime(event['datetime'], date_format).strftime("%H:%M:%S")
        this_event = datetime.strptime(event['datetime'], date_format)
        last_event = datetime.strptime(sorted_events[index - 1]['datetime'], date_format)
        delta = this_event - last_event
        if delta > timedelta(seconds=1):
            event['delta'] = str(delta).split(".")[0]
    return sorted_events


def petition_deadline(petition):
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    now = datetime.utcnow()

    deadline = {}
    if petition['data']['attributes']['open_at']:
        deadline_datetime = datetime.strptime(
            petition['data']['attributes']['open_at'], date_format
        ) + timedelta(days=182)
        deadline['datetime'] = deadline_datetime.strftime(date_format)
        deadline['date'] = deadline_datetime.strftime("%d %B %Y")
        deadline['time'] = deadline_datetime.strftime("%H:%M:%S")
        deadline['type'] = 'deadline'
        delta = deadline_datetime - now
        deadline['delta'] = str(delta).split(".")[0]
    else:
        deadline = None
    return deadline
