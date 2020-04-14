from tkinter import *

import requests
from xmltramp2 import xmltramp

from API.API_constants import *
import json

NAME = "OpenWeatherMap"

openweather_main_url = "https://api.openweathermap.org/data/2.5/weather?"
# openweather_appID = "75a90db613d4fa920dd60f4bb3be02ef"
# 75a90db613d4fa920dd60f4bb3be02ef

# Docs: https://openweathermap.org/api
from tkinter import StringVar

API_key = open("API/APIs/open_weather_map/API_key.txt").read()
API_key_tkvar: StringVar

city_list_file = open("API/APIs/open_weather_map/city_list.json", encoding="UTF-8").read()
city_list = json.loads(city_list_file, encoding="UTF-8")


def configure():
    global API_key
    API_key = API_key_tkvar.get()
    file = open("API/APIs/open_weather_map/API_key.txt", "w")
    file.write(API_key)
    file.close()

    print("[OpenWeatherMap API] API key set to", API_key_tkvar.get())


def config():
    global API_key, API_key_tkvar
    root = Tk()
    root.title("OpenWeatherMap API configuration")
    API_key_tkvar = StringVar()

    label = Label(master=root, justify=LEFT, text="API key:", anchor=W)
    label.pack(fill="x", padx=10, side=TOP)

    submit_frame = Frame(master=root)
    submit_frame.pack(side=TOP, fill=X)

    api_key_entry = Entry(master=submit_frame, justify=CENTER, textvariable=API_key_tkvar)
    api_key_entry.delete(0, END)
    api_key_entry.insert(0, API_key)
    api_key_entry.pack(fill=X, padx=10, side=LEFT, expand=1)

    submit_button = Button(master=submit_frame, text="configure", command=configure)
    submit_button.pack(side=LEFT, padx=10, fill=X)

    API_key_tkvar.set(API_key)

    root.mainloop()


CONFIG = config


def get_status():
    return ACTIVE


def build_request_string(bodystring: str, appid: str, cityname: str, country: str, XML: bool):
    # country: de, uk, us  ...
    # api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={your api key}
    # api.openweathermap.org/data/2.5/weather?id={city id}&appid={your api key}
    # api.openweathermap.org/data/2.5/find?q=London&units=metric&appid=75a90db613d4fa920dd60f4bb3be02ef
    # http://api.openweathermap.org/data/2.5/find?q=Frankfurt&units=metric&appid=75a90db613d4fa920dd60f4bb3be02ef&mode=xml
    # http://api.openweathermap.org/data/2.5/box/city?bbox=12,32,15,37,10&units=metric&appid=75a90db613d4fa920dd60f4bb3be02ef&mode=xml
    # https://openweathermap.org/current#data

    get_string = bodystring + "q=" + cityname + "," + country + "&appid=" + appid
    get_string = get_string + "&units=metric"  # hardcoded
    get_string = get_string + "&lang=de"  # hardcoded

    if XML:
        get_string = get_string + "&mode=xml"
    # debug
    # print(get_string)
    # back = requests.get(get_string)
    # print(back.text)
    return get_string


def decode_xmlstring(xmlstring):
    root = xmltramp.parse(xmlstring)
    # print(root.city("name"), ",", root.city.country, ':', root.temperature("value"),
    #      "(", root.temperature("min"), "/", root.temperature("max"), ")", root.temperature("unit"))

    db_entry = {
                   "temperature": {
                       "real": root.temperature("value"),
                       "felt": root.feels_like("value")
                   },
                   "wind": {
                       "direction": root.wind.direction("code"),
                       "degrees": root.wind.direction("value"),
                       "speed": root.wind.speed("value")
                   },
                   "clouds": {
                       "condition": {
                           "OpenWeatherMap": root.clouds("name")
                       }
                   },
                   "air": {
                       "view_distance": root.visibility("value"),
                       "pressure": root.pressure("value"),
                       "humidity": root.humidity("value")
                   }
               }
        #print(root)
    return db_entry

requ_string = build_request_string(openweather_main_url, API_key, "Leipzig", "de", True)
# print(back)
xmlback = requests.get(requ_string)
print(xmlback.text)
db_entry = decode_xmlstring(xmlback.text)
print(db_entry)