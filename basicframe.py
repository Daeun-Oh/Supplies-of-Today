import tkinter as tk
from tkinter import ttk
from tkinter import Label
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk
import requests

class MyApp:

    def __init__(self, parent):
        parent.geometry("1200x500")
        parent.title("오늘의 준비물✔️")

        # 프레임 분할
        self.frame = tk.Frame(parent, bg="#FFCC99")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # 왼쪽 프레임
        self.left_frame = tk.Frame(self.frame, bg="#FFCC99")
        self.left_frame.pack(side=tk.LEFT, anchor=tk.CENTER, padx=10, pady=10)

        # 검색 버튼
        self.search_button = ttk.Button(self.left_frame, text="검색")
        self.search_button.pack(pady=10)

        # 날씨 정보 프레임
        self.weather_info_frame = tk.Frame(self.left_frame, width=8, height=500, relief=tk.SOLID, borderwidth=1)
        self.weather_info_frame.pack(pady=10)

        # "오늘의 날씨 정보" 레이블
        self.weather_label = ttk.Label(self.weather_info_frame, text="체감온도: 🍒 ")
        self.weather_label.pack(pady=10)
        self.weather_label = ttk.Label(self.weather_info_frame, text="")
        self.weather_label.pack(pady=10)
        self.weather_label = ttk.Label(self.weather_info_frame, text="")
        self.weather_label.pack(pady=10)
        self.weather_label = ttk.Label(self.weather_info_frame, text="                      오늘의 날씨 정보                       ")
        self.weather_label.pack(pady=10)
        self.weather_label = ttk.Label(self.weather_info_frame, text="")
        self.weather_label.pack(pady=10)
        self.weather_label = ttk.Label(self.weather_info_frame, text="")
        self.weather_label.pack(pady=10)

        # 코디 추천 버튼
        url = "https://www.muji.com/wp-content/uploads/sites/12/2021/02/026.jpg"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        image1 = Image.open(BytesIO(raw_data))
        desired_width = 70
        desired_height = 70
        image1 = image1.resize((desired_width, desired_height))
        photo_image1 = ImageTk.PhotoImage(image1)

        self.button1 = ttk.Button(self.left_frame, image=photo_image1, command=self.recommend_outfit)
        self.button1.pack(side=tk.LEFT, padx=10, pady=10)
        self.button1.image = photo_image1


        # 카톡 공유 버튼
        url = "https://upload.wikimedia.org/wikipedia/commons/f/f2/Kakao_logo.jpg"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        image = Image.open(BytesIO(raw_data))
        desired_width = 70
        desired_height = 70
        image = image.resize((desired_width, desired_height))
        photo_image = ImageTk.PhotoImage(image)

        self.button2 = ttk.Button(self.left_frame, image=photo_image)
        self.button2.pack(side=tk.LEFT, padx=10, pady=10)
        self.button2.image = photo_image

        # 텔레그램 챗봇 버튼
        url = "https://img.etnews.com/photonews/1502/658167_20150225185759_549_0001.jpg"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        image3 = Image.open(BytesIO(raw_data))
        desired_width = 70
        desired_height = 70
        image3 = image3.resize((desired_width, desired_height))
        photo_image3 = ImageTk.PhotoImage(image3)

        self.button3 = ttk.Button(self.left_frame, image=photo_image3)
        self.button3.pack(side=tk.LEFT, padx=10, pady=10)
        self.button3.image = photo_image3



        # 오른쪽 프레임
        self.right_frame = tk.Frame(self.frame)
        self.right_frame.pack(side=tk.LEFT, expand=True)

        # 그래프 분할
        self.graph_frame = tk.Frame(self.right_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # 그래프 1
        self.graph1 = tk.Frame(self.graph_frame, bg="white")
        self.graph1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.figure1 = Figure(figsize=(4, 4), dpi=100)
        self.plot1 = self.figure1.add_subplot(111)
        self.plot1.plot([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])

        self.canvas1 = FigureCanvasTkAgg(self.figure1, master=self.graph1)
        self.canvas1.draw()
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.label1 = tk.Label(self.graph1, text="강수량 그래프", justify=tk.CENTER)
        self.label1.pack(side=tk.TOP)

        # 그래프 2
        self.graph2 = tk.Frame(self.graph_frame, bg="white")
        self.graph2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.figure2 = Figure(figsize=(4, 4), dpi=100)
        self.plot2 = self.figure2.add_subplot(111)
        self.plot2.plot([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])

        self.canvas2 = FigureCanvasTkAgg(self.figure2, master=self.graph2)
        self.canvas2.draw()
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.label2 = tk.Label(self.graph2, text="미세먼지 농도 그래프", justify=tk.CENTER)
        self.label2.pack(side=tk.TOP)

    #코디추천 버튼 클릭
    def recommend_outfit(self):
        url = "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzA0MjFfMTYz%2FMDAxNjgyMDY2OTAxMzc2.4yht1NWPfgMSw3cSiBrZfRYjc5IvM4PT5GW55oeuKC4g.sUKzfzC7SO3u9T20cHn3qRNhnJsZ2pmcXAqxPooDW98g.JPEG.dayoung828%2F%25B1%25E2%25BF%25C2%25BA%25B0_%25BF%25CA%25C2%25F7%25B8%25B2_%25B2%25DC%25C6%25C1.jpg&type=sc960_832"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()

        # 이미지를 표시할 새로운 창 생성
        outfit_window = tk.Toplevel()
        outfit_window.title("온도에 따른 코디 👗")
        outfit_window.geometry("1000x1000")

        self.image = Image.open(BytesIO(raw_data))
        self.photo_image = ImageTk.PhotoImage(self.image)
        label = Label(outfit_window, image=self.photo_image, height=1000, width=1000)
        label.pack()


root = tk.Tk()
myapp = MyApp(root)
root.mainloop()
