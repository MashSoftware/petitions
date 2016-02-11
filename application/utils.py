import json
import requests
import geojson
from geojson import Polygon, Feature, FeatureCollection

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
