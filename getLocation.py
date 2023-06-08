from geopy.geocoders import Nominatim
import json
import requests

def geocoding(address):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    geo = geolocoder.geocode(address)
    crd = {"lat": str(geo.latitude), "lng": str(geo.longitude)}

    return crd

def geocoding_reverse(lat_lng_str):
    geolocoder = Nominatim(user_agent = 'South Korea', timeout=None)
    address = geolocoder.reverse(lat_lng_str)
    # 주소
    text = ""
    address = str(address)
    address = address.split(", ")
    print(address)
    msgAddr = []
    msgAddr.append(address[-3])
    msgAddr.append(address[-4])
    if msgAddr[0] != "세종":
        if msgAddr[1][-1] != "군":
            if len(address) > 5 and address[-6][-2].isdigit():
                msgAddr.append(address[-6])
            else:
                msgAddr.append(address[-5])
        else:
            msgAddr.append(address[-5])
    print(msgAddr)

    for lm in msgAddr:
        text += lm + " "
    text = text[:-1]

    return text

def get_currLocation():
    url = 'http://www.geoplugin.net/json.gp?'
    response = requests.get(url)
    data = json.loads(response.text)
    return data