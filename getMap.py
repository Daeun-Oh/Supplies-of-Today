#현재 좌표의 지도로 띄우기 - 첫번째 프레임에 띄우기 - 지도 배치확인
#api_key = AIzaSyB2d8ZBeA7WoD3v4cbsgihUvC1IbmrrAIU

from getLocation import *
import webbrowser
import folium

# 현재 좌표 정보 받아오기
location_data = get_currLocation()
current_location = {'lat': location_data['geoplugin_latitude'], 'lng': location_data['geoplugin_longitude']}

# 사용자의 Google Maps API 키
api_key = "AIzaSyB2d8ZBeA7WoD3v4cbsgihUvC1IbmrrAIU"

# 지도 생성
m = folium.Map(location=[float(current_location['lat']), float(current_location['lng'])], zoom_start=15, API_key=api_key)
folium.Marker(location=[float(current_location['lat']), float(current_location['lng'])], popup='현재 위치').add_to(m)
m.save('map.html')

# 지도 파일 열기
webbrowser.open('map.html')