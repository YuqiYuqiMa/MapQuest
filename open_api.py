### open_api

import urllib.parse
import urllib.request
import json

### this module buils up url links
# builds the url for location with a list of locations
# buils the url for elevation with a list of lat and long

### gets json objects
# uses open_url to open webpage, download file, and decode
# finally gets json object

### json object can be used in other modules

API_KEY = 'bMAohW5yWMGQANtpGC1ExZDhQ7LK0MGF'
BASE_URL = 'http://open.mapquestapi.com/directions/v2/route?key='

ELEVATION_URL = 'http://open.mapquestapi.com/elevation/v1/profile?key='
URL_TAIL = '&shapeFormat=raw&latLngCollection='

def build_location_url(location_list: list) -> str:
    '''
    build up a valid url link with a list of locations
    '''
    url = BASE_URL + API_KEY
    new_location = []
    new_location.append(("from", location_list[0]))
    for num in range(1, len(location_list)):
        new_location.append(("to", location_list[num]))       
    locality = urllib.parse.urlencode(new_location)
    final_url = url + "&" + locality
    return final_url


def build_elevation_url(latlong: list) -> 'json':
    '''
    builds up a valid url link for elevation
    returns a url link
    '''
    new_url = ELEVATION_URL + API_KEY + URL_TAIL
    for item in latlong:
        new_url += str(item)
        new_url += ','
    new_url = new_url[:-1]
    return new_url


def open_url(query: str) -> 'json':
    '''
    opens the url link and returns a json response
    using the given string of url link
    '''
    json_obj = urllib.request.urlopen(query)
    response = json_obj.read().decode(encoding = 'utf-8')
    data = json.loads(response)
    return data
