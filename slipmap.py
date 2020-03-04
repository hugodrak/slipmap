import requests
from bs4 import BeautifulSoup
import os
import json
# https://weather.com/weather/today/l/57.71,11.92?temp=c
BASE_URL = "https://weather.com/weather/today/l/"

origin = 'Göteborg'
destination = 'Borås'
MAPS_URL = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={os.environ['gmaps_key']}"

def dict_pretty_print(indict):
    print("-----------------------")
    for key, value in indict.items():
        print("%s: %s" % (key, value))
    print("-----------------------")

def f2c(temp_f: float):
    return (temp_f - 32) * (5/9)

def get_weather_data(lat, long):
    r = requests.get(f"{BASE_URL}{lat},{long}")
    soup = BeautifulSoup(r.text, 'html.parser')
    current_weather = soup.find_all('div', {'class': 'today_nowcard'})[0]
    side_card = current_weather.find_all('div', {'class': 'today_nowcard-sidecar'})[0].contents[0].contents[1].contents
    temp = current_weather.find_all('div', {'class': 'today_nowcard-temp'})[0].contents[0].text[:-1]

    temp_int = format(f2c(float(temp)), '.4f') # f => c
    wind = side_card[0].text[4:].split(" ")
    wind_dir = wind[0]
    wind_int = format(float(wind[1])*0.44704, '.4f') # mph => m/s
    hum = format(float(side_card[1].text[8:-1]), '.4f')
    dew = format(f2c(float(side_card[2].text[9:-1])), '.4f')
    press = format(float(side_card[3].text[8:-4])/0.029529983071445, '.4f')
    vis = format(float(side_card[4].text[10:-3])*1.609344, '.4f')

    weather = [f'{lat},{long}', {'temperature': [temp_int, 'C'], 'windDirection': [wind_dir, 'dir'], 'windSpeed': [wind_int, 'm/s'], 'humidity': [hum, '%'], 'dewPoint': [dew, 'C'], 'airPressure': [press, 'kPa'], 'visibility': [vis, 'Km']}]
    return weather

def get_route(url):
    r = requests.get(url)
    json_raw = r.json()
    steps = json_raw['routes'][0]['legs'][0]['steps']
    for step in steps:
        lat, long = step['start_location']['lat'], step['start_location']['lng']
        print(get_weather_data(lat, long)[1]['temperature'])

# data = get_weather_data(57.71,11.92)
# print(data[0])
# dict_pretty_print(data[1])
get_route(MAPS_URL)
