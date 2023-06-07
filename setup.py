import os
import glob
from distutils.core import setup, Extension

# 압축을 푼 파일의 경로를 얻어옵니다.
base_path = os.path.dirname(os.path.abspath(__file__))

setup(
    name='testSoT',
    version='1.0',
    py_modules=['Supplies-of-Today', 'getLocation', 'getWeather', 'getFineDust', 'getMap', 'CopyToClipboard', 'noti', 'teller'],
    ext_modules=[Extension('comparingkv', ['comparingkvmodule.c'])],
    data_files=[
        (base_path, ['sunny.png', 'cloudy.png', 'very_cloudy.png', 'rainy.png', 'clipboard.png', 'clothes.png', 'telegram.png']),
        ('fashionImages', glob.glob('fashionImages/*')),
        (base_path, ['Dovemayo_gothic.ttf']),
        (base_path, ['location_data.xlsx'])
    ]
)
