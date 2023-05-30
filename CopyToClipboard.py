import pyperclip as pc
import datetime
from getWeather import getWeather
from getFineDust import getNowAirPollution
from getLocation import geocoding_reverse
def copyToClipboard(ix, iy, msg2_5, msg10):
    print("실행합니다")
    pm2_5, pm10 = getNowAirPollution(ix, iy)
    pm2_5, pm10 = float(pm2_5), float(pm10)
    addr = geocoding_reverse(str(ix) + ", " + str(iy))
    print(addr)
    #print(type(addr))
    addr = str(addr)
    addr = addr.split(", ")
    msgAddr = [addr[i] for i in range(-1,-6,-2)]
    print(msgAddr)

    times = ['02', '05', '08', '11', '14', '17', '20', '23']
    now = datetime.datetime.now()
    currentHour = now.hour
    for i in range(len(times)):
        if int(times[i]) > int(currentHour):
            currentHour = times[i-1]
            break
    currWeather = getWeather(ix, iy, currentHour+'00', '97')
    print(currWeather)

    hours = []
    precipitation = []
    temperatures = []
    precipitationRate = []
    isRainy = False
    # 데이터 추출
    for hour, info in currWeather.items():
        hours.append(str(hour)[:-2])
        if info['1시간강수량'] == '강수없음':
            precipitation.append(0.0)
        else:
            precipitation.append(float(info['1시간강수량'][:-2]))
            isRainy = True
        precipitationRate.append(info['강수확률'])
        temperatures.append(info['1시간기온'])

    text = "── ❝ 𝐒𝐮𝐩𝐩𝐥𝐢𝐞𝐬 𝐨𝐟 𝐓𝐨𝐝𝐚𝐲 ❞ ──\n" \
           "☂️: "
    if isRainy:
        text += "O    "
    else:
        text += "X    "
    text += "😷: "
    if msg2_5 == "나쁨" or msg2_5 == "매우나쁨" or msg10 == "나쁨" or msg10 == "매우나쁨":
        text += "O\n\n"
    else:
        text += "X\n\n"
    text += "위치: "
    for l in msgAddr:
        text += l + ", "
    text = text[:-2] + "\n"
    text += "초미세먼지: " + str(pm2_5) + " ㎍/m³ (" + msg2_5 + ")\n"
    text += "미세먼지: " + str(pm10) + " ㎍/m³ (" + msg10 + ")\n"
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
    pc.copy(text)
    # a1 = "ᴠᴏʟᴜᴍᴇ : ▮▮▮▮▮▮▯▯▯\n" \
    #     "i'm daeun oh\n" \
    #     "are you happy?\n" \
    #     "this is python\n" \
    #     "copy\n" \
    #     "&\n" \
    #     "paste!\n" \
    #     "* 。 • ˚ ˚ ˛ ˚ ˛ • 。*"
    # pc.copy(a1)
#copyToClipboard(37.5576, 126.9937, )