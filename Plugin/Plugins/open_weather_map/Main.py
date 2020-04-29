import json
from tkinter import *
import time
import requests
from ttk import *
from xmltramp2 import xmltramp

import Core.error_handler as eh
from Plugin.API_constants import *

NAME = "OpenWeatherMap"

openweather_url_bodies = {"current_weather_data": "https://api.openweathermap.org/data/2.5/weather?"}
# openweather_appID = "75a90db613d4fa920dd60f4bb3be02ef"
# 75a90db613d4fa920dd60f4bb3be02ef

# Docs: https://openweathermap.org/api
from tkinter import StringVar

API_key = open("Plugin/Plugins/open_weather_map/API_key.txt").read()
API_key_tkvar: StringVar

print("[OpenWeatherMap] loading database...")
city_list_file = open("Plugin/Plugins/open_weather_map/city_list.json", encoding="UTF-8").read()
city_list = json.loads(city_list_file, encoding="UTF-8")
print("[OpenWeatherMap] ... finished!")


def configure():
    global API_key
    API_key = api_key_entry.get()
    file = open("API/APIs/open_weather_map/API_key.txt", "w")
    file.write(API_key)
    file.close()

    print("[OpenWeatherMap API] API key set to", API_key)


def test():
    requ_string = build_request_string(openweather_url_bodies["current_weather_data"], API_key, "Berlin", "de", True)
    try:
        answer = requests.get(requ_string)
    except requests.ConnectionError:
        return SERVER_NOT_RESPONDING
    if answer.status_code == 200:
        return WORKING
    elif answer.status_code == 401:
        return WRONG_API_KEY
    else:
        eh.error("Invalid response: " + answer.text)
        return ERROR


def config():
    global api_key_entry
    root = Tk()
    root.title("OpenWeatherMap API configuration")

    label = Label(master=root, justify=LEFT, text="API key:", anchor=W)
    label.pack(fill="x", padx=10, side=TOP)

    submit_frame = Frame(master=root)
    submit_frame.pack(side=TOP, fill=X)

    api_key_entry = Entry(master=submit_frame, justify=CENTER)
    api_key_entry.delete(0, END)
    api_key_entry.insert(0, API_key)
    api_key_entry.pack(fill=X, padx=10, side=LEFT, expand=1)

    submit_button = Button(master=submit_frame, text="configure", command=configure)
    submit_button.pack(side=LEFT, padx=10, fill=X)

    root.mainloop()


def get_status():
    return test()


def format(city):
    return f"{city['name']} - {city['country']}"


def search_city_list(search_string):
    return [city for city in city_list if search_string.lower() in city["name"].lower()][:2000]


def build_request_string(bodystring: str, appid: str, cityname: str, country: str, XML: bool = True):
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

    # print(root)
    return db_entry


def current_weather(timestamp):
    xmlstring = build_request_string(openweather_url_bodies[0], API_key, "Leipzig", "de", True)
    root = xmltramp.parse(xmlstring)

    weather = {
        "temperature_real": True,
        "temperature_felt": True,
        "humidity": True,
        "pressure": True,
        "wind_speed": True,
        "wind_direction": True,
        "wind_direction_name": True,
        "wind_direction_code": True,
        "clouds_name": True,
        "view_distance": True,
        "precipitation": True,
        "weather_name": True
    }

    astronomy = {

    }

    return {"weather": {}, "astronomy": {}}


def current_weather_scheduler(schedules):
    t = time.time()
    return [schedule for schedule in schedules if not (schedule[3] in ["temperature_real",
                                                                       "temperature_felt",
                                                                       "humidity",
                                                                       "pressure",
                                                                       "wind_speed",
                                                                       "wind_direction",
                                                                       "wind_direction_name",
                                                                       "wind_direction_code",
                                                                       "clouds_name",
                                                                       "view_distance",
                                                                       "precipitation",
                                                                       "weather_name",
                                                                       "sun_set",
                                                                       "sun_rise"
                                                                       ] and (t-schedule[2]))]


api_functions = [
    (current_weather, current_weather_scheduler)

]

# {"temperature_real": True,
#  "temperature_felt": True,
#  "humidity": True,
#  "pressure": True,
#  "wind_speed": True,
#  "wind_direction": True,
#  "wind_direction_name": True,
#  "wind_direction_code": True,
#  "clouds_name": True,
#  "view_distance": True,
#  "precipitation": True,
#  "weather_name": True}

# requ_string = build_request_string(openweather_main_url, API_key, "Leipzig", "de", True)
# # print(back)
# xmlback = requests.get(requ_string)
# print(xmlback.text)
# db_entry = decode_xmlstring(xmlback.text)
# print(db_entry)
api_key_entry: Entry
