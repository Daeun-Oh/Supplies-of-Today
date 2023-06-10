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
from CopyToClipboard import copyToClipboard
from getWeather import getWeather
from getFineDust import getNowAirPollution, getNowAirPollutionMassage
import datetime
from getLocation import geocoding_reverse, geocoding


import noti

t_lat, t_lng, t_msg2_5, t_msg10 = 0.0, 0.0, "", ""
def getInfo(lat, lng, msg2_5, msg10):
    global t_lat, t_lng, t_msg2_5, t_msg10
    t_lat, t_lng, t_msg2_5, t_msg10 = lat, lng, msg2_5, msg10
    telepot_run()

def chatbot(ix, iy, msg2_5, msg10, a):
    print("실행합니다")
    pm2_5, pm10 = getNowAirPollution(ix, iy)
    pm2_5, pm10 = float(pm2_5), float(pm10)
    addr = geocoding_reverse(str(ix) + ", " + str(iy))

    times = ['02', '05', '08', '11', '14', '17', '20', '23']
    now = datetime.datetime.now()
    currentHour = now.hour
    for i in range(len(times)):
        if int(times[i]) > int(currentHour):
            currentHour = times[i - 1]
            break
    currWeather = getWeather(ix, iy, str(currentHour) + '00', '290')  # 97
    print(currWeather)

    hours = []
    precipitation = []
    temperatures = []
    precipitationRate = []
    isRainy = False
    # 데이터 추출
    for hour, info in currWeather.items():
        if int(hour) < int(str(currentHour) + '00'):
            continue
        hours.append(str(hour)[:-2])
        if info['1시간강수량'] == '강수없음':
            precipitation.append(0.0)
        else:
            precipitation.append(float(info['1시간강수량'][:-2]))
            isRainy = True
        precipitationRate.append(info['강수확률'])
        temperatures.append(info['1시간기온'])
        if hour == '2300':
            break
    today = datetime.date.today()
    todayDate = today.strftime('%Y%m%d')
    todayDate = todayDate.replace('0', '𝟶').replace('1', '𝟷').replace('2', '𝟸').replace('3', '𝟹') \
        .replace('4', '𝟺').replace('5', '𝟻').replace('6', '𝟼').replace('7', '𝟽').replace('8', '𝟾').replace('9', '𝟿')
    currTime = now.strftime("%H:%M")
    currTime = currTime.replace('0', '𝟶').replace('1', '𝟷').replace('2', '𝟸').replace('3', '𝟹') \
        .replace('4', '𝟺').replace('5', '𝟻').replace('6', '𝟼').replace('7', '𝟽').replace('8', '𝟾').replace('9', '𝟿')

    if a==1:
        text = "위치: "+addr+"\n"

        text += "☂️: "
        if isRainy:
            text += "O    "
        else:
            text += "X    "
        text += "😷: "
        if msg2_5 == "나쁨" or msg2_5 == "매우나쁨" or msg10 == "나쁨" or msg10 == "매우나쁨":
            text += "O\n\n"
        else:
            text += "X\n\n"

        print(text)
        return text

    elif a==2: #날씨
        text = "위치: "+addr+"\n"

        text += "현재 기온: " + str(temperatures[0]) + " ℃\n"

        text += "강수 예상 시간: "
        if isRainy:
            for i in range(len(hours)):
                if precipitation[i] != 0.0:
                    text += hours[i] + "시, "
            text = text[:-2]
        else:
            text += "X"

        print(text)
        return text

    elif a==3: #미세먼지
        text = "위치: "+addr+"\n"

        text += "초미세먼지: " + str(pm2_5) + " ㎍/m³ (" + msg2_5 + ")\n"
        text += "미세먼지: " + str(pm10) + " ㎍/m³ (" + msg10 + ")\n"

        print(text)
        return text


def handle(msg):
    global t_lat

    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '텍스트 이외의 메시지는 처리하지 못해요')
        return

    text = msg['text']
    args = text.split(', ')

    if text.startswith('명령어'):
        noti.sendMessage(chat_id, '[명령어 목록]\n'
                                  '전체: 프로그램 내에서 검색한 위치의 전체 정보를 출력합니다!\n'
                                  '준비물: 프로그램 내에서 검색한 위치의 준비물 정보를 출력합니다!'
                                  '\n날씨: 프로그램 내에서 검색한 위치의 날씨 정보를 출력합니다!\n'
                                  '미세먼지: 프로그램 내에서 검색한 위치의 미세먼지 정보를 출력합니다!\n'
                                  '검색, [지역]: 입력하신 지역의 전체 정보를 출력합니다!')

    elif text.startswith('전체'):
        output_text = copyToClipboard(t_lat, t_lng, t_msg2_5, t_msg10)
        noti.sendMessage(chat_id, output_text)

    elif text.startswith('준비물'):
        output_text = chatbot(t_lat, t_lng, t_msg2_5, t_msg10, 1)
        noti.sendMessage(chat_id, output_text)

    elif text.startswith('날씨'):
        output_text = chatbot(t_lat, t_lng, t_msg2_5, t_msg10, 2)
        noti.sendMessage(chat_id, output_text)

    elif text.startswith('미세먼지'):
        output_text = chatbot(t_lat, t_lng, t_msg2_5, t_msg10, 3)
        noti.sendMessage(chat_id, output_text)

    elif text.startswith('검색') and len(args) > 1:
        print('try to 검색')
        search_location = geocoding(args[1])
        search_msg2_5, search_msg10 = getNowAirPollutionMassage(float(search_location['lat']), float(search_location['lng']))
        output_text = copyToClipboard(float(search_location['lat']), float(search_location['lng']), search_msg2_5, search_msg10)
        noti.sendMessage(chat_id, output_text)

    else:
        noti.sendMessage(chat_id, '[명령어 목록]\n전체, 준비물, 날씨, 미세먼지 중 하나의 명령을 입력하세요.')

def telepot_run():
    today = date.today()
    current_month = today.strftime('%Y%m')

    print('[', today, '] received token:', noti.TOKEN)

    bot = telepot.Bot(noti.TOKEN)
    pprint(bot.getMe())

    bot.message_loop(handle)

    print('Listening...')

    # while True:
    #     time.sleep(10)
