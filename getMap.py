#현재 좌표의 지도로 띄우기 - 첫번째 프레임에 띄우기 - 지도 배치확인
#api_key = AIzaSyB2d8ZBeA7WoD3v4cbsgihUvC1IbmrrAIU
from getLocation import *
import tkinter as tk
import webbrowser

# 현재 좌표 정보
# 현재 좌표 정보 받아오기
location_data = get_currLocation()
current_location = {'lat': location_data['geoplugin_latitude'], 'lng': location_data['geoplugin_longitude']}


# 네이버 지도 API 요청을 위한 함수
def get_google_map_url(location):
    api_key = "AIzaSyB2d8ZBeA7WoD3v4cbsgihUvC1IbmrrAIU"
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={location['lat']},{location['lng']}&zoom=12&size=800x600&maptype=roadmap&key={api_key}"
    return url

# 버튼 클릭 이벤트 핸들러
def show_map():
    url = get_google_map_url(current_location)
    webbrowser.open(url)

# tkinter 윈도우 생성
window = tk.Tk()
window.title("Google 지도")
window.geometry("400x300")

# 버튼 생성
button = tk.Button(window, text="지도 보기", command=show_map)
button.pack(pady=10)

# 윈도우 실행
window.mainloop()
