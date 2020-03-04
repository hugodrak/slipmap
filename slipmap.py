import requests
from bs4 import BeautifulSoup
import os
# https://weather.com/weather/today/l/57.71,11.92?temp=c
BASE_URL = "https://weather.com/weather/today/l/"



def get_data(lat, long):
    r = requests.get(f"{BASE_URL}{lat},{long}?temp=c")
    soup = BeautifulSoup(r.text, 'html.parser')
    current_weather = soup.find_all('div', {'class': 'today_nowcard'})[0]
    temp = current_weather.find_all('div', {'class': 'today_nowcard-temp'})[0].contents[0].text[:-1]
    side_card = current_weather.find_all('div', {'class': 'today_nowcard-sidecar'})[0].contents[0].contents[1].contents

    temp_int = (int(temp) - 32) * (5/9)
    wind = side_card[0].text[4:]
    hum = side_card[1].text[8:]
    dew = side_card[2].text[10:]
    press = side_card[3].text[8:]
    vis = side_card[4].text[10:]

    weather = [temp_int, wind, hum, dew, press, vis]
    print(weather)
    h = 0

get_data(57.71,11.92)
