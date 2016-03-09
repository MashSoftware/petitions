import json
import requests
import geojson
from geojson import Polygon, Feature, FeatureCollection
from operator import itemgetter
from datetime import datetime, timedelta

def get_mp(constituency):
    api_key = 'GEd7VBGHYis2AAXETMAhu9YD'
    response = requests.get('http://www.theyworkforyou.com/api/getMP?key=' + api_key + '&constituency=' + constituency + '&output=js')
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        data = response.json()
    return data

def constituency_extent(ons_code):
    response =  requests.get('http://mapit.mysociety.org/area/' + ons_code + '.geojson')
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        data = response.json()
    return data

def constituency_collection(constituencies):
    features=[]

    for constituency in constituencies [:10]:
        feature = Feature(geometry=Polygon(constituency_extent(constituency['ons_code'])['coordinates']))
        feature.properties['name'] = constituency['name']
        feature.properties['mp'] = constituency['mp']
        feature.properties['party'] = constituency['party']
        feature.properties['url'] = constituency['url']
        feature.properties['signature_count'] = constituency['signature_count']
        features.append(feature)

    feature_collection = FeatureCollection(features)

    return geojson.dumps(feature_collection)

def petition_events(petition):
    events=[]
    date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    for k,v in petition['data']['attributes'].items():
        if '_at' in k:
            if v is not None:
                event={}
                event['datetime'] = v
                event['type'] = k
                events.append(event)


    sorted_events = sorted(events, key=itemgetter('datetime'))
    for index, event in enumerate(sorted_events):
        event['date'] = datetime.strptime(event['datetime'],date_format).strftime("%d %B %Y")
        event['time'] = datetime.strptime(event['datetime'],date_format).strftime("%H:%M:%S")
        this_event = datetime.strptime(event['datetime'],date_format)
        last_event = datetime.strptime(sorted_events[index -1]['datetime'],date_format)
        delta = this_event - last_event
        if delta > timedelta(seconds=1):
            event['delta'] = str(delta).split(".")[0]
    return sorted_events
