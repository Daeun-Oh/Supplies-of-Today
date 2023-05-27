from tkinter import *
from tkinter import font, Canvas
from getMap import *
from getLocation import *
from getWeather import getWeather
from getFineDust import getNowAirPollution
from PIL import Image, ImageTk, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm
import urllib.request
import numpy as np


# 위치 정보 가져오기
location_data = get_currLocation()

class ProjectSoT:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x500")
        self.window.title("오늘의 준비물✔️")

        self.frame1 = Frame(self.window, bg = '#FFCC99', width=1200, height=500)    # 지도 띄우는 창
        self.frame2 = None    # 그래프 띄우는 창

        # frame1에서 쓰이는 변수
        self.locationAddr = {}
        self.locationCoor = {"lat": str(location_data['geoplugin_latitude']),
                        "lng": str(location_data['geoplugin_longitude'])}

        # frame2에서 쓰이는 변수
        self.hours = []                 # 읽어온 시간
        self.temperatures = []         # 기온
        self.sky = ''                   # 하늘상태
        self.precipitation = []         # 강수량
        self.precipitationRate = []     # 강수확률

        self.img_tk = None

        self.InitFrame1()

    def InitFrame1(self):
        print("프레임1 입장")
        print("현재 좌표:", self.locationCoor)
        self.frame1.place(x=0, y=0, width=1200, height=500)

        self.leftFrame1 = Frame(self.frame1, bg="#FFCC99")
        self.leftFrame1.place(x=0, y=0, width=400, height=500)

        self.rightFrame1 = Frame(self.frame1, bg='yellow')
        self.rightFrame1.place(x=400, y=0, width=800, height=500)

        setup(self.rightFrame1)

        self.SearchFont = font.Font(size=15, family='Dovemayo_gothic')
        self.ButtonFont = font.Font(size=11, family='Dovemayo_gothic')
        self.label = Label(self.leftFrame1, text="주소 검색창", font=self.SearchFont, bg='#FFCC99')
        self.entry = Entry(self.leftFrame1, font=self.SearchFont)
        self.label.pack()
        self.entry.pack()

        Button(self.leftFrame1, text="  날씨  ", font=self.ButtonFont, command=self.moveToFrame2).pack()
        Button(self.leftFrame1, text="  지도  ", font=self.ButtonFont, command=self.reloadMap).pack()
        # def label_click(event):
        #     show_map()

        # underline_font = font.Font(family="Dovemayo_gothic", size=11, underline=True)
        # label = tk.Label(self.frame1, text="지도를 보고싶으면 클릭하세요", bg="#FFCC99", fg="#000000", font=underline_font)
        # label.pack()

        # label.bind("<Button-1>", label_click)

    def saveLocation(self): # frame1의 보기 버튼 누르면 실행
        if str(self.entry.get()) == "":
            print("검색이 안 됨")
        else:
            self.locationAddr = str(self.entry.get())
            self.locationCoor = geocoding(self.locationAddr)

    def reloadMap(self):
        self.saveLocation()
        reloadMap([float(self.locationCoor['lat']),self.locationCoor["lng"]])
    def InitFrame2(self):
        print("프레임2 입장")
        self.frame2 = Frame(self.window, bg='#FFCC99', width=1200, height=500)
        weather = getWeather(round(float(self.locationCoor['lat']), 4), round(float(self.locationCoor['lng']), 4))
        self.frame2.place(x=0, y=0, width=1200, height=500)


        self.leftFrame2 = Frame(self.frame2, bg="#FFCC99")
        self.leftFrame2.place(x=0, y=50, width=400, height=450, anchor='nw')

        self.rightFrame2 = Frame(self.frame2, bg="#FFCC99")
        self.rightFrame2.place(x=400, y=0, width=800, height=500, anchor='nw')


        buttonS = Button(self.leftFrame2, text="    검색    ", font=self.ButtonFont, command=self.moveToFrame1)
        buttonS.place(x=200, y=0, anchor='n')

        print("현재 주소:", self.locationAddr)
        print("현재 좌표:", self.locationCoor)

        ############################################
        buttonX = 50 + 25
        buttonY = 330

        # 코디 추천 버튼

        imageC = Image.open("clothes.png")  # 이미지 파일
        imageC = imageC.resize((70, 70))  # 이미지 크기 조정

        photoC = ImageTk.PhotoImage(imageC)

        self.button1 = Button(self.leftFrame2, bg='white', image=photoC, command=self.recommend_outfit)
        self.button1.place(x=buttonX, y=buttonY)
        self.button1.image = photoC

        # 카카오톡 버튼

        buttonX += 90

        imageK = Image.open("kakao.png")  # 이미지 파일
        imageK = imageK.resize((70, 70))  # 이미지 크기 조정

        photoK = ImageTk.PhotoImage(imageK)

        self.button2 = Button(self.leftFrame2, bg='white', image=photoK)
        self.button2.place(x=buttonX, y=buttonY)
        self.button2.image = photoK

        # 텔레그램 버튼

        buttonX += 90

        imageT = Image.open("telegram.png")  # 이미지 파일
        imageT = imageT.resize((70, 70))  # 이미지 크기 조정

        photoT = ImageTk.PhotoImage(imageT)

        self.button3 = Button(self.leftFrame2, bg='white', image=photoT)
        self.button3.place(x=buttonX, y=buttonY)
        self.button3.image = photoT

        ##########################################

        #i = 0
        #for key in list(weather.keys()):
        #    #print(i, w)
        #    if i < 1:
        #        del(weather[key])
        #    i += 1
        #print(weather)

        # 데이터 추출
        for hour, info in weather.items():
            self.hours.append(str(hour)[:-2])
            if info['1시간강수량'] == '강수없음':
                self.precipitation.append(0.0)
            else:
                self.precipitation.append(float(info['1시간강수량'][:-2]))
            self.precipitationRate.append(info['강수확률'])
            self.temperatures.append(info['1시간기온'])
        self.sky = weather[list(weather.keys())[0]]['하늘상태']
        print(self.temperatures)
        print(self.precipitation)
        print(self.precipitationRate)
        print("하늘: "+self.sky)

        ## 날씨 + 미세먼지 ##
        if int(self.sky) < 6:
            weatherImage = Image.open("sunny.png")  # 맑음
        elif int(self.sky) < 9:
            weatherImage = Image.open("cloudy.png")  # 구름많음
        elif int(self.sky) < 11:
            weatherImage = Image.open("very_cloudy.png")  # 흐림

        weatherImage = weatherImage.resize((300, 240))  # 이미지 크기 조정

        # 텍스트 설정
        msg2_5, msg10 = self.fineDust()
        text1 = "초미세먼지: "+msg2_5
        text2 = "미세먼지: "+msg10
        font_size = 15  # 폰트 크기
        font = ImageFont.truetype("Dovemayo_gothic.ttf", font_size)  # 폰트 설정

        # 이미지에 텍스트 그리기
        draw = ImageDraw.Draw(weatherImage)
        text1_bbox = draw.textbbox((0, 0, weatherImage.width, weatherImage.height), text1, font=font)
        text1_width = text1_bbox[2] - text1_bbox[0]
        text1_height = text1_bbox[3] - text1_bbox[1]
        text1_position = ((weatherImage.width - text1_width) // 2, 5)  # 텍스트 위치 조정
        draw.text(text1_position, text1, font=font, fill="black")
        text2_bbox = draw.textbbox((0, 0, weatherImage.width, weatherImage.height), text2, font=font)
        text2_width = text2_bbox[2] - text2_bbox[0]
        text2_height = text2_bbox[3] - text2_bbox[1]
        text2_position = ((weatherImage.width - text2_width) // 2, text2_height+10)  # 텍스트 위치 조정
        draw.text(text2_position, text2, font=font, fill="black")

        # 이미지를 Tkinter에서 사용할 수 있는 형식으로 변환
        photo = ImageTk.PhotoImage(weatherImage)
        label_image = Label(self.leftFrame2, image=photo)
        label_image.image = photo
        label_image.place(x=200, y=60, anchor="n")

        ## 그래프 ##
        font_path = 'Dovemayo_gothic.ttf'
        GraphFont = fm.FontProperties(fname=font_path, size=15, weight='bold')

        self.graph1 = Frame(self.rightFrame2, width=400, height=500)
        self.graph1.pack(side=LEFT)

        fig = Figure(figsize=(4, 4), facecolor="#FFCC99", dpi=100)
        ax1 = fig.add_subplot(111)
        ax1_t = ax1.twinx()     # 강수량 y축

        # 막대 그래프
        x_bar = np.arange(len(self.precipitationRate))
        ax1.bar(x_bar, self.precipitationRate, label='rate', color="#9CB8BC")

        # 선형 그래프
        x_linear = np.arange(len(self.precipitation))
        ax1_t.plot(x_linear, self.precipitation, marker='', label='precipitation', color="#718F8E")

        ax1.set_title('강수 그래프', fontproperties=GraphFont, pad=20)

        # x축 눈금의 위치와 레이블 설정
        xticks_pos = range(len(self.hours))
        ax1.set_xticks(xticks_pos)
        ax1.set_xticklabels(self.hours, rotation='vertical')

        # 두 y축 범례를 하나의 범례로 표시
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax1_t.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='best')

        # 왼쪽 y축 범위 설정
        ax1.set_ylim(0.0, 100.0)

        # 오른쪽 y축 범위 설정
        if all(value == 0.0 for value in self.precipitation):
            ax1_t.set_ylim(0.0, 1.0)  # 모든 값이 0.0인 경우에는 0.0부터 1.0까지의 범위로 설정
        elif max(self.precipitation) <= 5.0:
            ax1_t.set_ylim(0.0, 5.0)
        else:
            ax1_t.set_ylim(min(self.precipitation), max(self.precipitation))

        canvas = FigureCanvasTkAgg(fig, master=self.graph1)
        canvas.draw()
        canvas.get_tk_widget().pack(side='left')

        # 기온 막대 그래프
        self.graph2 = Frame(self.rightFrame2, width=400, height=550)
        self.graph2.pack(side=LEFT)

        fig2 = Figure(figsize=(4, 4), facecolor="#FFCC99", dpi=100)
        ax2 = fig2.add_subplot(111)

        ax2.bar(x_bar, self.temperatures, color="#D6B3A6", label="temperature")  # 추가 데이터를 막대 그래프로 그림
        ax2.set_title('기온 그래프', fontproperties=GraphFont, pad=20)

        ax2.set_xticks(xticks_pos)
        ax2.set_xticklabels(self.hours, rotation='vertical')

        ax2.legend()

        canvas2 = FigureCanvasTkAgg(fig2, master=self.graph2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side='left')

    def fineDust(self):
        pm2_5, pm10 = getNowAirPollution(self.locationCoor['lat'], self.locationCoor['lng'])
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

        return msg2_5, msg10

    def recommend_outfit(self):
        fashionImage = Image.open("fashion.png")
        fashionImage = fashionImage.resize((496, 662))  # 이미지 크기 조정

        # 이미지를 Tkinter에서 사용할 수 있는 형식으로 변환
        self.img_tk = ImageTk.PhotoImage(fashionImage)

        # 이미지를 표시할 새로운 창 생성
        outfit_window = Toplevel(self.window)
        outfit_window.title("온도에 따른 코디 👗")

        label = Label(outfit_window, image=self.img_tk, width=496, height=662)
        label.pack()

    def moveToFrame2(self):
        self.frame1.pack_forget()  # frame1 숨기기
        if self.frame2 is not None:
            self.hours = []  # 읽어온 시간
            self.temperatures = []  # 기온
            self.sky = ''  # 하늘상태
            self.precipitation = []  # 강수량
            self.precipitationRate = []  # 강수확률

            self.img_tk = None
            self.frame2.destroy()
        self.InitFrame2()

    def moveToFrame1(self):
        self.saveLocation()
        self.frame2.place_forget()  # owindow 최소화
        self.frame1.pack(fill="both", expand=True)   # swindow 표시

    def run(self):
        self.window.mainloop()

project = ProjectSoT()
project.run()