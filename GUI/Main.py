from tkinter import *
import Core.error_handler as eh
import API.API_constants as api_constants
from threading import Thread


def quit():
    global _mainloop
    print("[GUI] Window close button event, terminating.")
    _mainloop = False
    root.destroy()


def format(city):
    return f"{city['name']} - {city['country']} {city['state']}({city['id']})"


def mainloop(core_main):
    global city

    def set_city(event):
        global city
        city = cities_objects[search_list_box.curselection()[0]]
        print(city)
        search_bar.delete(0, END)
        search_bar.insert(0, cities[search_list_box.curselection()[0]])

    search_list_box.bind("<Double-Button-1>", set_city)

    open_weather_map_api = [api for api in core_main.apis if api.NAME == "OpenWeatherMap"][0]
    if not open_weather_map_api:
        eh.error("Preview of Cities not possible because there is no API-moule named \"OpenWeatherMap\"")

    if not root:
        raise Exception("[GUI] No main Window created.")

    error_count = 0
    max_errors = 10
    prevtext = search_bar.get()

    while _mainloop:
        try:
            root.update()
            text = search_bar.get()
            if (text != "") and (text != format(city)) and (text != prevtext):
                print("UPDATE")
                prevtext = text
                city = {"name": None, "id": None, "state": None, "country": None}
                search_list_box_frame.pack(fill=BOTH, expand=1, padx=10)

                cities = [format(cityi) for cityi in open_weather_map_api.city_list if
                          text.lower() in cityi['name'].lower()][:200]
                cities_objects = [cityi for cityi in
                                  open_weather_map_api.city_list if text.lower() in cityi['name'].lower()][:200]
                search_list_box.delete(0, END)
                status_bar.config(text="Loading cities...")
                i = 0
                for cityi in cities:
                    search_list_box.insert(END, cityi)
                    if i % 20 == 0:
                        root.update()
                    i += 1
                status_bar.config(text="Ready...")
                search_list_box.config(height=len(cities))

            elif (text == prevtext) and (not city["name"]):
                pass
            else:
                search_list_box_frame.pack_forget()

            if city["name"]:
                select_city_info_label.config(text=f"Lat: {city['coord']['lat']}, Lon: {city['coord']['lon']}")
            else:
                select_city_info_label.config(text="Please select a city.")

        except TclError as e:
            print("[GUI] TclError occurred:", e)
            error_count += 1
            if error_count >= max_errors:
                eh.error(f"[GUI] Maximum error count of {max_errors} exceeded, terminating.")


def open_api_config(core_main):
    core_main.apis[api_list_box.curselection()[0]].CONFIG()


def start(core_main):
    def mouse_wheel(event):
        scroll = round(event.delta / 60) * -1
        api_list_box.yview("scroll", scroll, "units")
        api_status_list_box.yview("scroll", scroll, "units")
        return "break"

    global root, search_bar, menu_bar, api_list_box, search_list_box_frame, status_bar, search_list_box, \
        select_city_info_label
    root = Tk()
    root.title("WeatherViewer by JHondah and Belissimo")
    root.protocol("WM_DELETE_WINDOW", quit)

    menu_bar = Menu(master=root)
    # MENU CONFIGURATION -------------------------------------------------------
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_radiobutton(label="Germany")
    edit_menu.add_radiobutton(label="UK/USA")
    edit_menu.invoke(0)
    menu_bar.add_cascade(label="Localization", menu=edit_menu)

    api_menu = Menu(menu_bar, tearoff=0)
    for api in core_main.apis:
        api_menu.add_command(label=api.NAME, command=api.CONFIG)
    menu_bar.add_cascade(label="APIs", menu=api_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    menu_bar.add_cascade(label="Help", menu=help_menu)
    # MENU CONFIGURATION END ---------------------------------------------------
    root.config(menu=menu_bar)

    status_bar = Label(master=root, bg="#E0E0E0", text="Ready...", anchor=W)
    status_bar.pack(fill=X, side=BOTTOM)

    control_frame = Frame(master=root)
    control_frame.pack(side=TOP, fill=BOTH)

    select_city_frame = LabelFrame(master=control_frame, relief=RIDGE, borderwidth=5, text="Area Selection")
    select_city_frame.pack(fill=X, side=LEFT, anchor=N, expand=1)

    Label(master=select_city_frame, text="Type the name of the city or area you want to have the weather data of:",
          justify=LEFT, anchor=W).pack(side=TOP, pady=10, fill=BOTH, padx=10)

    select_city_info_label = Label(master=select_city_frame, anchor=W, text="Please select a city.")
    select_city_info_label.pack(side=BOTTOM, anchor=S, fill=X, expand=1, padx=10)

    search_bar = Entry(master=select_city_frame)
    search_bar.pack(side=TOP, pady=5, fill=BOTH, padx=10)

    search_list_box_frame = Frame(master=select_city_frame)
    search_list_box = Listbox(master=search_list_box_frame)
    search_list_box.pack(fill=BOTH, expand=1, anchor=N, side=LEFT)
    search_scrollbar = Scrollbar(master=search_list_box_frame, command=search_list_box.yview)
    search_list_box.config(yscrollcommand=search_scrollbar.set)
    search_scrollbar.pack(side=LEFT, anchor=N, fill=Y)

    apis_frame = LabelFrame(master=control_frame, relief=RIDGE, borderwidth=5, text="API Manager", labelanchor=N)
    apis_frame.pack(fill=X, side=RIGHT, anchor=N)

    apis_text_frame = Frame(master=apis_frame)
    apis_text_frame.pack(fill=X, side=TOP, anchor=N, expand=1)

    Label(master=apis_text_frame, text="APIs:").pack(fill=X, side=LEFT, expand=1)
    Label(master=apis_text_frame, text="Statuses:").pack(fill=X, side=LEFT, expand=1)

    listbox_frame = Frame(master=apis_frame)
    listbox_frame.pack(side=TOP, fill=BOTH, expand=1)

    api_list_box = Listbox(master=listbox_frame, selectmode=SINGLE)
    api_list_box.pack(side=LEFT, expand=1, fill=BOTH)

    api_list_box.bind("<Double-Button-1>", lambda event: open_api_config(core_main))

    api_status_list_box = Listbox(master=listbox_frame, selectmode=SINGLE)
    api_status_list_box.pack(side=LEFT, expand=1, fill=BOTH)

    for api in core_main.apis:
        api_list_box.insert(END, api.NAME)
        api_status_list_box.insert(END, api_constants.statuses[api.get_status()])

    api_scrollbar = Scrollbar(master=listbox_frame, orient=VERTICAL,
                              command=lambda *args: (api_list_box.yview(*args), api_status_list_box.yview(*args)))

    api_list_box.config(yscrollcommand=api_scrollbar.set)
    api_status_list_box.config(yscrollcommand=api_scrollbar.set)

    api_list_box.bind("<MouseWheel>", mouse_wheel)
    api_status_list_box.bind("<MouseWheel>", mouse_wheel)

    api_scrollbar.pack(side=LEFT, fill=Y)

    weather_frame = LabelFrame(master=root, relief=RIDGE, borderwidth=5, text="Weather")
    weather_frame.pack(side=BOTTOM, expand=1, fill=BOTH, anchor=S)

    Canvas(master=weather_frame, bg="red").pack()

    mainloop(core_main)

city = {"name": None, "id": None, "state": None, "country": None}
root: Tk
search_bar: Entry
menu_bar: Menu
_mainloop = True
api_list_box: Listbox
search_list_box_frame: Frame
status_bar: Label
search_list_box: Listbox
select_city_info_label: Label
