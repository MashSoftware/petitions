import json
import requests

def get_mp_data(constituency):
    api_key = app.config['TWFY_API_KEY']

    response = requests.get('http://www.theyworkforyou.com/api/getMP?key=' + api_key + '&constituency=' + constituency + '&output=js')
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        data = response.json()
    return data

def get_constitiency_extent(ons_code):
    response =  requests.get('http://mapit.mysociety.org/area/' + ons_code + '.geojson')
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    else:
        data = response.text
    return data
