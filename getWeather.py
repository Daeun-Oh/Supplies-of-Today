from urllib.request import urlopen
from urllib.parse import urlencode, unquote, quote_plus
import urllib
import requests
import json
from xml.etree.ElementTree import parse
import xmltodict
import pandas as pd
import datetime
import math

NX = 149            ## X축 격자점 수
NY = 253            ## Y축 격자점 수

Re = 6371.00877     ##  지도반경
grid = 5.0          ##  격자간격 (km)
slat1 = 30.0        ##  표준위도 1
slat2 = 60.0        ##  표준위도 2
olon = 126.0        ##  기준점 경도
olat = 38.0         ##  기준점 위도
xo = 210 / grid     ##  기준점 X좌표
yo = 675 / grid     ##  기준점 Y좌표
first = 0

if first == 0 :
    PI = math.asin(1.0) * 2.0
    DEGRAD = PI/ 180.0
    RADDEG = 180.0 / PI


    re = Re / grid
    slat1 = slat1 * DEGRAD
    slat2 = slat2 * DEGRAD
    olon = olon * DEGRAD
    olat = olat * DEGRAD

    sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(PI * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(PI * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    first = 1

def mapToGrid(lat, lon, code = 0 ):
    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI :
        theta -= 2.0 * PI
    if theta < -PI :
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y

def gridToMap(x, y, code = 1):
    x = x - 1
    y = y - 1
    xn = x - xo
    yn = ro - y + yo
    ra = math.sqrt(xn * xn + yn * yn)
    if sn < 0.0 :
        ra = -ra
    alat = math.pow((re * sf / ra), (1.0 / sn))
    alat = 2.0 * math.atan(alat) - PI * 0.5
    if math.fabs(xn) <= 0.0 :
        theta = 0.0
    else :
        if math.fabs(yn) <= 0.0 :
            theta = PI * 0.5
            if xn < 0.0 :
                theta = -theta
        else :
            theta = math.atan2(xn, yn)
    alon = theta / sn + olon
    lat = alat * RADDEG
    lon = alon * RADDEG

    return lat, lon

def getWeather(ix, iy, t, rows):
    (x, y) = mapToGrid(ix, iy)
    print(x, y)
    # API 요청 주소와 필요한 매개변수 설정
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    ServiceKey = 'YwHylQNXuEGl%2FSgiCsShpt85OlqItTNEzeSzgNg9%2BQPtuyOXN6LRX3TmCVUemaPkn92eMyGp9VQxbKmSWdsubw%3D%3D'
    today = datetime.date.today()
    now = datetime.datetime.now()
    baseData = today.strftime('%Y%m%d')

    ##
    times = ['02', '05', '08', '11', '14', '17', '20', '23']
    now = datetime.datetime.now()
    currentHour = now.hour
    for i in range(len(times)):
        if int(times[i]) > int(currentHour):
            currentHour = times[i - 1]
            break
    baseTime = str(currentHour)+'00'
    ##

    if rows == '290':
        baseData = str(int(baseData)-1)
    #baseTime = t
    #baseTime = now.strftime('%H')
    #if int(baseTime) == 0:
    #    baseTime = '23'
    #    baseData = str(int(baseData)-1)
    #else:
    #    baseTime = str(int(baseTime) - 1)
    #    if len(baseTime) != 2:
    #        baseTime = '0'+baseTime
    #baseTime += '00'
    #print(baseData, baseTime)

    queryParams = '?' + urlencode(
        {
            quote_plus('ServiceKey') : ServiceKey,
            quote_plus('numOfRows') : rows,    #290, 한 줄 당?
            quote_plus('dataType') : 'JSON',
            quote_plus('base_date') : baseData,
            quote_plus('base_time') : baseTime,
            quote_plus('nx') : x,
            quote_plus('ny') : y
        }
    )
    request = urllib.request.Request(url + unquote(queryParams))
    response_body = urlopen(request).read() # get bytes data
    #print(response_body)
    decode_data = response_body.decode('utf-8')
    print(decode_data)

    # JSON 데이터를 파싱하여 딕셔너리로 변환
    data = json.loads(decode_data)
    print(data)

    # 데이터 가공
    forcast = {}
    for i, info in enumerate(data['response']['body']['items']['item']):
        if i >= 0:
            if info['fcstTime'] not in forcast:
                forcast[info['fcstTime']] = {}

            if info['category']== 'POP':
                forcast[info['fcstTime']]['강수확률'] = float(info['fcstValue'])
                #print('category:강수확률,', info['category'], 'baseTime:', info['baseTime'], ', fcstTime:', info['fcstTime'], ', fcstValue:', info['fcstValue'])
            elif info['category']== 'PTY':
                forcast[info['fcstTime']]['강수형태'] = float(info['fcstValue'])
                #print('category:강수형태,', info['category'], 'baseTime:', info['baseTime'], ', fcstTime:', info['fcstTime'], ', fcstValue:', info['fcstValue'])
            elif info['category']== 'PCP':
                forcast[info['fcstTime']]['1시간강수량'] = info['fcstValue']
                #print('category:1시간강수량,', info['category'], 'baseTime:', info['baseTime'], ', fcstTime:', info['fcstTime'], ', fcstValue:', info['fcstValue'])
            elif info['category'] == 'SKY':
                forcast[info['fcstTime']]['하늘상태'] = info['fcstValue']   # 0-5: 맑음 / 6-8: 구름많음 / 9-10: 흐림
            elif info['category']== 'TMP':
                forcast[info['fcstTime']]['1시간기온'] = float(info['fcstValue'])
                #print('category:1시간기온,', info['category'], 'baseTime:', info['baseTime'], ', fcstTime:', info['fcstTime'], ', fcstValue:', info['fcstValue'])

    print(forcast)
    return forcast