#해야할것
#두번째 창 위치 연동
#입력한 키워드별 정보 출력

#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
from CopyToClipboard import copyToClipboard
from getMap import *
from getLocation import *
from getWeather import getWeather
from getFineDust import getNowAirPollution

import noti

location_data = get_currLocation()
locationCoor = {"lat": str(location_data['geoplugin_latitude']), "lng": str(location_data['geoplugin_longitude'])} #현재 위치정보만을 확인. 검색창에 입력한 위치정보는 확인불가.

pm2_5, pm10 = getNowAirPollution(locationCoor['lat'], locationCoor['lng'])
pm2_5, pm10 = float(pm2_5), float(pm10)
print(pm2_5, pm10)
if pm2_5 <= 15.0:
    msg2_5 = "좋음"
elif pm2_5 <= 35.0:
    msg2_5 = "보통"
elif pm2_5 <= 75.0:
    msg2_5 = "나쁨"
else:
    msg2_5 = "매우나쁨"

if pm10 <= 30.0:
    msg10 = "좋음"
elif pm10 <= 80.0:
    msg10 = "보통"
elif pm10 <= 150.0:
    msg10 = "나쁨"
else:
    msg10 = "매우나쁨"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '텍스트 이외의 메시지는 처리하지 못해요')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('안녕'):
        noti.sendMessage(chat_id, '오늘의 준비물 봇 입니다. \n 모든 정보를 확인하고 싶으면 "전체"를 입력하세요!')

    elif text.startswith('전체'):
        output_text = copyToClipboard(round(float(locationCoor['lat']), 4), round(float(locationCoor['lng']), 4), msg2_5, msg10)
        noti.sendMessage(chat_id, output_text)

    elif text.startswith('준비물'):
        output_text = copyToClipboard(round(float(locationCoor['lat']), 4), round(float(locationCoor['lng']), 4), msg2_5, msg10)
        noti.sendMessage(chat_id, output_text)

    elif text.startswith('날씨'):
        output_text = copyToClipboard(round(float(locationCoor['lat']), 4), round(float(locationCoor['lng']), 4), msg2_5, msg10)
        noti.sendMessage(chat_id, output_text)

    elif text.startswith('미세먼지'):
        output_text = copyToClipboard(round(float(locationCoor['lat']), 4), round(float(locationCoor['lng']), 4), msg2_5, msg10)
        noti.sendMessage(chat_id, output_text)

    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n전체, 준비물, 날씨, 미세먼지 중 하나의 명령을 입력하세요.')


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )


bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)