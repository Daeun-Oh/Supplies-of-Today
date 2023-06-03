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
    currWeather = getWeather(ix, iy, str(currentHour)+'00', '290')    # 97
    print(currWeather)

    hours = []
    precipitation = []
    temperatures = []
    precipitationRate = []
    isRainy = False
    # 데이터 추출
    for hour, info in currWeather.items():
        if int(hour) < int(str(currentHour)+'00'):
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
    todayDate = todayDate.replace('0', '𝟶').replace('1', '𝟷').replace('2', '𝟸').replace('3', '𝟹')\
        .replace('4', '𝟺').replace('5', '𝟻').replace('6', '𝟼').replace('7', '𝟽').replace('8', '𝟾').replace('9', '𝟿')
    currTime = now.strftime("%H:%M")
    currTime = currTime.replace('0', '𝟶').replace('1', '𝟷').replace('2', '𝟸').replace('3', '𝟹')\
        .replace('4', '𝟺').replace('5', '𝟻').replace('6', '𝟼').replace('7', '𝟽').replace('8', '𝟾').replace('9', '𝟿')


    text = "── ❝ 𝐒𝐮𝐩𝐩𝐥𝐢𝐞𝐬 𝐨𝐟 𝐓𝐨𝐝𝐚𝐲 ❞ ──\n"
    text += "𝙳𝚊𝚝𝚎 · "+todayDate+"\n"
    text += "𝚃𝚒𝚖𝚎 · "+currTime+"\n"
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

    return text
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