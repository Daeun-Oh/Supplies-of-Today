from getLocation import *
import tkinter as tk
import webview
import folium
import sys
from cefpython3 import cefpython as cef
import threading
from PIL import ImageTk, Image

browser = None

def setup(frame):

    # 현재 좌표 정보 받아오기
    location_data = get_currLocation()
    current_location = {'lat': location_data['geoplugin_latitude'], 'lng': location_data['geoplugin_longitude']}

    # 사용자의 Google Maps API 키
    api_key = "API_KEY"

    # 지도 생성
    m = folium.Map(location=[float(current_location['lat']), float(current_location['lng'])], zoom_start=15)

    # 현재 위치에 마커 추가
    folium.Marker(location=[float(current_location['lat']), float(current_location['lng'])], popup='현재 위치').add_to(m)

    # 지도를 HTML 파일로 저장
    m.save("map.html")

    # 브라우저를 위한 쓰레드 생성
    thread = threading.Thread(target=showMap, args=(frame,)) #왜 showMap아래에 빨간줄이 생긴거지
    thread.daemon = True
    thread.start()

def showMap(frame):
    global browser
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), [0,0,800,600])
    cef.Initialize()
    browser = cef.CreateBrowserSync(window_info, url='file:///map.html')
    cef.MessageLoop()

def reloadMap(loc, bookmarks):
    # print(bookmarks)
    text = geocoding_reverse(str(loc[0]) + ", " + str(loc[1]))

    m = folium.Map(location=loc, zoom_start=13)
    folium.Marker(loc, popup=text).add_to(m)

    for bm in bookmarks:
        # 주소
        text = geocoding_reverse(str(bm[0]) + ", " + str(bm[1]))
        # 마킹
        folium.Marker(bm, popup=text, icon=folium.Icon(color='orange', icon='star')).add_to(m)

    m.save('map.html')
    browser.Reload()
# WebView 실행 함수 호출
# show_map()