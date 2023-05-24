from tkinter import *
from tkinter import font, Canvas
from getLocation import *
from getWeather import getWeather
from PIL import Image, ImageTk



# 위치 정보 가져오기
location_data = get_currLocation()

class ProjectSoT:
    locationAddr = {}
    locationCoor = {"lat": str(location_data['geoplugin_latitude']), "lng": str(location_data['geoplugin_longitude'])}


    def __init__(self):
        self.window = Tk()
        self.window.geometry("1200x500")
        self.window.title("오늘의 준비물✔️")

        self.frame1 = Frame(self.window, bg = '#FFCC99', width=1200, height=500)    # 지도 띄우는 창
        self.frame2 = Frame(self.window)    # 그래프 띄우는 창

        self.InitFrame1()

    def InitFrame1(self):
        print("프레임1 입장")
        print("현재 좌표:", self.locationCoor)
        self.frame1.grid(row=0, column=0)

        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')
        self.label = []  # 라벨 배열
        self.entry = []
        self.label.append(Label(self.frame1, text="안녕", font=self.TempFont, bg='#FFCC99'))
        self.label[0].grid(row=0, column=0)

        self.entry.append(Entry(self.frame1, font=self.TempFont))
        self.entry[0].grid(row=0, column=1)

        Button(self.frame1, text="보기", font=self.TempFont, command=self.saveLocation).grid(row=11, column=0)

    def saveLocation(self): # frame1의 보기 버튼 누르면 실행
        self.locationAddr = str(self.entry[0].get())
        self.locationCoor = geocoding(self.locationAddr)
        self.frame1.grid_forget()  # frame1 숨기기
        self.InitFrame2()

    def InitFrame2(self):
        print("프레임2 입장")
        weather = getWeather(round(float(self.locationCoor['lat']), 4), round(float(self.locationCoor['lng']), 4))
        self.frame2.grid(row=0, column=0)

        self.weatherFrame = Frame(self.frame2, width=500, height=600, bg='#FFCC99')
        self.weatherFrame.grid(row=0, column=0)

        # 이미지 로드
        image = Image.open("sunny.png")  # 이미지 파일
        image = image.resize((300, 300))  # 이미지 크기 조정

        # 이미지를 Tkinter에서 사용할 수 있는 형식으로 변환
        photo = ImageTk.PhotoImage(image)
        label = Label(self.weatherFrame, image=photo)
        label.image = photo
        label.grid(row=1, column=0)

        button = Button(self.weatherFrame, text="검색", font=self.TempFont, command=self.moveToFrame1)
        button.grid(row=0, column=0)

        print("현재 주소:", self.locationAddr)
        print("현재 좌표:", self.locationCoor)

        i = 0
        for key in list(weather.keys()):
            #print(i, w)
            if i < 5:
                del(weather[key])
            i += 1
        print(weather)

        # 데이터 추출
        print("그려보자")
        hours = []
        temperatures = []
        for hour, info in weather.items():
            hours.append(str(hour))
            temperatures.append(info['1시간기온'])
        print(temperatures)

        cw, ch = 1000, 1000
        cr, cc = 800, 800
        canvas = Canvas(self.frame2, width=cw, height=ch)
        canvas.grid(row=cr, column=cc)

        # 기온 막대 그래프
        maxT = max(temperatures)
        x1 = 200
        y1 = 300
        for i in range(len(temperatures)):
            canvas.create_rectangle(x1, y1, x1+30, y1-200*temperatures[i]/maxT, fill='blue')
            canvas.create_text(x1+15, y1+10, text=hours[i][:2]+':'+hours[i][2:], font=('Arial', 10))
            x1 += 40
        canvas.create_rectangle(200-50, y1+50, 200+40*len(temperatures)+50, y1-200-50, outline='black', width=2)

    def moveToFrame1(self):
        self.frame2.grid_forget()  # owindow 최소화
        self.InitFrame1()   # swindow 표시


    def run(self):
        self.window.mainloop()

project = ProjectSoT()
project.run()