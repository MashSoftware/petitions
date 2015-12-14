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
