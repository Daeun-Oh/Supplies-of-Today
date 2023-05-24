from geopy.geocoders import Nominatim
import json
import requests

def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd

def get_currLocation():
    url = 'http://www.geoplugin.net/json.gp?'
    response = requests.get(url)
    data = json.loads(response.text)
    return data