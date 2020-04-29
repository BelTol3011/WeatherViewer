# Powered by WeatherAPI.com
from tkinter import *
from Plugin.API_constants import *

# a1433a15876943eb9cc104305201404

API_key = open("Plugin/Plugins/weather_api/API_key.txt").read()
API_key_tkvar: StringVar


def configure():
    global API_key
    API_key = API_key_tkvar.get()
    file = open("Plugin/Plugins/WeatherAPI/API_key.txt", "w")
    file.write(API_key)
    file.close()
    print("[WeatherAPI] API key set to", API_key)


def config():
    global API_key, API_key_tkvar
    root = Tk()
    root.title("WeatherAPI configuration")
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


def get_status():
    return UNKNOWN


def format(city):
    return city["name"]


def nullo(lol):
    return [{"name": "This is a city", "country": "DE", "coord": {"lat": 0, "lon": -0}}]


def nullol(lol):
    return lol["name"]


NAME = "WeatherAPI"
CONFIGURE = config
