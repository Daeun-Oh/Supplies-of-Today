#작은 문제점: 내 좌표가 실제좌표와 다름
#첫번째 프레임에 띄우기 - 지도 배치확인
#api_key = AIzaSyB2d8ZBeA7WoD3v4cbsgihUvC1IbmrrAIU

#엄청난 문제점: entry(검색창)이 안 먹힘
#예상 이유: 지도가 무한루프라 메인 윈도우창의 이벤트 루프가 시작되지 않음 (근데 클릭은 됨)
#chat gpt는 threading 모듈을 통해
#Tkiner 이벤트 루프는 메인 스레드에서 실행하고,
#웹뷰는 별도의 스레드에서 실행하여 두 가지를 동시에 작동시키라고 함.
#근데 가능할지는 모르겠음
#대안: entry는 없애고 지역 선택으로 바꾸기
#일단 entry 살리는 거 시도해보고, 대안을 적용시키는 걸로...

from getLocation import *
import tkinter as tk
import webview
import folium
import sys
from cefpython3 import cefpython as cef
import threading

browser = None

def setup(frame):
    # 현재 좌표 정보 받아오기
    location_data = get_currLocation()
    current_location = {'lat': location_data['geoplugin_latitude'], 'lng': location_data['geoplugin_longitude']}

    # 사용자의 Google Maps API 키
    api_key = "YOUR_API_KEY"

    # 지도 생성
    m = folium.Map(location=[float(current_location['lat']), float(current_location['lng'])], zoom_start=15)

    # 현재 위치에 마커 추가
    folium.Marker(location=[float(current_location['lat']), float(current_location['lng'])], popup='현재 위치').add_to(m)

    # 지도를 HTML 파일로 저장
    m.save("map.html")

    # 브라우저를 위한 쓰레드 생성
    thread = threading.Thread(target=showMap, args=(frame,))
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

def reloadMap(loc):
    m = folium.Map(location=loc, zoom_start=13)
    folium.Marker(loc, popup='서울대').add_to(m)
    m.save('map.html')
    browser.Reload()
# WebView 실행 함수 호출
# show_map()