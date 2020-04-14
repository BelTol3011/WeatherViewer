# Powered by WeatherAPI.com
from tkinter import *

API_key = "a1433a15876943eb9cc104305201404"
API_key_tkvar: StringVar


def configure():
    global API_key
    API_key = API_key_tkvar.get()
    print("[WeatherAPI] API key set to", API_key)


def config():
    global API_key, API_key_tkvar
    root = Tk()
    root.title("WeatherAPI configuration")
    API_key_tkvar = StringVar()

    label = Label(master=root, justify=CENTER, text="API key:")
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


NAME = "WeatherAPI"
CONFIG = config
