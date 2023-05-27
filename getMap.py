#작은 문제점: 내 좌표가 실제좌표와 다름
#첫번째 프레임에 띄우기 - 지도 배치확인
#api_key = AIzaSyB2d8ZBeA7WoD3v4cbsgihUvC1IbmrrAIU

from getLocation import *
import tkinter as tk
import webview
import folium

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

# WebView 윈도우 실행
def show_map():
    webview.create_window("Interactive Map", "map.html", width=800, height=600, resizable=True)
    webview.start()

# WebView 실행 함수 호출
# show_map()

