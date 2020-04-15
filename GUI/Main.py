from tkinter import *
from ttk import *
import Core.error_handler as eh
import API.API_constants as api_constants
from threading import Thread
from ttkthemes import themed_tk


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
        latitude_entry.delete(0, END)
        longitude_entry.delete(0, END)
        latitude_entry.insert(0, city["coord"]["lat"])
        longitude_entry.insert(0, city["coord"]["lon"])
        latitude_entry.config(state=DISABLED)
        longitude_entry.config(state=DISABLED)
        search_bar.delete(0, END)
        search_bar.insert(0, format(cities_objects[search_list_box.curselection()[0]]))

    search_list_box.bind("<Double-Button-1>", set_city)

    open_weather_map_api = [api for api in core_main.apis if api.NAME == "OpenWeatherMap"][0]
    if not open_weather_map_api:
        eh.error("Preview of Cities not possible because there is no API-module named \"OpenWeatherMap\"")

    if not root:
        raise Exception("[GUI] No main Window created.")

    error_count = 0
    max_errors = 10
    prevtext = search_bar.get()

    while _mainloop:
        try:
            root.update()

            # City Select ----------------------------------------------------------------
            text = search_bar.get()
            if (text != "") and (text != format(city)) and (text != prevtext):
                latitude_entry.config(state=NORMAL)
                longitude_entry.config(state=NORMAL)
                latitude_entry.delete(0, END)
                longitude_entry.delete(0, END)
                prevtext = text
                city = {"name": None, "id": None, "state": None, "country": None}
                search_list_box_frame.pack(fill=BOTH, expand=1, padx=10)
                cities_objects = [cityi for cityi in
                                  open_weather_map_api.city_list if text.lower() in format(cityi).lower()][:500]

                search_list_box.delete(0, END)
                status_bar.config(text="Searching trough cities...")
                root.update()
                i = 6
                for cityi in cities_objects:
                    search_list_box.insert(END, format(cityi))
                    if i % 10 == 0:
                        root.update()
                    # i += 1
                root.update()
                status_bar.config(text="Ready...")
                search_list_box.config(height=len(cities_objects))

            elif (text == prevtext) and (not city["name"]):
                pass
            else:
                search_list_box_frame.pack_forget()

            if city["name"] or (latitude_entry.get() and longitude_entry.get()):
                select_city_info_label.config(text="City or area selected.")
            else:
                select_city_info_label.config(text="Or enter latitude and longitude of you location.")

            if (latitude_entry.get() and longitude_entry.get()) and (not city["name"]):
                search_bar.delete(0, END)
                search_bar.config(state=DISABLED)
                search_list_box_frame.pack_forget()
                prevtext = ""
            elif not (latitude_entry.get() and longitude_entry.get()):
                search_bar.config(state=NORMAL)

            if (text == "") and city["name"]:
                city = {"name": None, "id": None, "state": None, "country": None}
                latitude_entry.config(state=NORMAL)
                longitude_entry.config(state=NORMAL)
                latitude_entry.delete(0, END)
                longitude_entry.delete(0, END)

            if text == "":
                prevtext = ""
            # City Select ----------------------------------------------------------------





        except TclError as e:
            print("[GUI] TclError occurred:", e)
            error_count += 1
            if error_count >= max_errors:
                eh.error(f"[GUI] Maximum error count of {max_errors} exceeded, terminating.")


def change_theme():
    global THEME
    THEME = theme_var.get()
    root.destroy()
    start(CORE_MAIN)


def open_api_config(core_main):
    core_main.apis[api_list_box.curselection()[0]].CONFIG()


def start(core_main):
    def mouse_wheel(event):
        scroll = round(event.delta / 60) * -1
        api_list_box.yview("scroll", scroll, "units")
        api_status_list_box.yview("scroll", scroll, "units")
        return "break"

    global root, search_bar, menu_bar, api_list_box, search_list_box_frame, status_bar, search_list_box, \
        select_city_info_label, latitude_entry, longitude_entry, theme_var, CORE_MAIN, api_status_list_box
    CORE_MAIN = core_main
    root = themed_tk.ThemedTk(theme=THEME)
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

    display_menu = Menu(menu_bar, tearoff=0)
    themes_menu = Menu(display_menu, tearoff=0)

    theme_var = StringVar()

    themes_menu.add_radiobutton(label="none", variable=theme_var, command=change_theme)
    themes_menu.add_separator()
    themes_menu.add_command(label="GNU GPLv3 Themes")
    themes_menu.add_radiobutton(label="arc", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="equilux", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="itft1", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="ubuntu", variable=theme_var, command=change_theme)
    themes_menu.add_separator()
    themes_menu.add_command(label="Tcl-License Themes")
    themes_menu.add_radiobutton(label="aquativo", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="black", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="blue", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="clearlooks", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="elegance", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="keramik", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="kroc", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="plastik", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="radiance", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="smog", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="scid", variable=theme_var, command=change_theme)
    themes_menu.add_radiobutton(label="winxpblue", variable=theme_var, command=change_theme)
    theme_var.set(THEME)

    display_menu.add_cascade(label="Themes", menu=themes_menu)
    menu_bar.add_cascade(label="Display", menu=display_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    menu_bar.add_cascade(label="Help", menu=help_menu)
    # MENU CONFIGURATION END ---------------------------------------------------
    root.config(menu=menu_bar)

    status_bar = Label(master=root, text="Ready...", anchor=W)
    # status_bar = Label(master=root, bg="#E0E0E0", text="Ready...", anchor=W)
    status_bar.pack(fill=X, side=BOTTOM)

    bottom_paned_window = PanedWindow(master=root, orient=VERTICAL)
    bottom_paned_window.pack(fill=BOTH, expand=1)

    main_paned_window = PanedWindow(master=bottom_paned_window, orient=HORIZONTAL)
    # main_paned_window.pack(side=TOP, fill=BOTH)
    bottom_paned_window.add(main_paned_window)

    select_city_frame = LabelFrame(master=main_paned_window, relief=GROOVE, borderwidth=5, text="Area Selection")
    # select_city_frame.pack(fill=X, side=LEFT, anchor=N, expand=1)
    main_paned_window.add(select_city_frame)

    Label(master=select_city_frame, text="Type the name of the city or area you want to have the weather data of:",
          justify=LEFT, anchor=W).pack(side=TOP, pady=10, fill=BOTH, padx=10)

    bottom_city_selection_frame = Frame(master=select_city_frame)
    bottom_city_selection_frame.pack(side=BOTTOM, fill=X, anchor=S, padx=10, expand=1)

    select_city_info_label_frame = Frame(master=bottom_city_selection_frame)
    select_city_info_label_frame.pack(side=LEFT)

    select_city_info_label = Label(master=select_city_info_label_frame, anchor=W,
                                   text="Or enter latitude and longitude of you location.")
    select_city_info_label.pack()
    select_city_info_label.propagate(0)

    latlon_frame = Frame(master=bottom_city_selection_frame)
    latlon_frame.pack(side=RIGHT)

    Label(master=latlon_frame, text="Lat.:").pack(side=LEFT, expand=1)

    latitude_entry = Entry(master=latlon_frame)
    latitude_entry.pack(side=LEFT, anchor=W, fill=X, expand=1)

    Label(master=latlon_frame, text="Lon.:").pack(side=LEFT, expand=1)

    longitude_entry = Entry(master=latlon_frame)
    longitude_entry.pack(side=LEFT, anchor=W, fill=X, expand=1)

    search_bar = Entry(master=select_city_frame)
    search_bar.pack(side=TOP, pady=5, fill=BOTH, padx=10)

    search_list_box_frame = Frame(master=select_city_frame)
    search_list_box = Listbox(master=search_list_box_frame)
    search_list_box.pack(fill=BOTH, expand=1, anchor=N, side=LEFT)
    search_scrollbar = Scrollbar(master=search_list_box_frame, command=search_list_box.yview)
    search_list_box.config(yscrollcommand=search_scrollbar.set)
    search_scrollbar.pack(side=LEFT, anchor=N, fill=Y)

    apis_frame = LabelFrame(master=main_paned_window, relief=GROOVE, borderwidth=5, text="API Manager", labelanchor=N)
    # apis_frame.pack(fill=X, side=RIGHT, anchor=N)
    main_paned_window.add(apis_frame)

    apis_text_frame = Frame(master=apis_frame)
    apis_text_frame.pack(fill=X, side=TOP, anchor=N, expand=1)

    Label(master=apis_text_frame, text="APIs:").pack(fill=X, side=LEFT, expand=1)
    Label(master=apis_text_frame, text="Statuses:").pack(fill=X, side=LEFT, expand=1)

    listbox_frame = Frame(master=apis_frame)
    listbox_frame.pack(side=TOP, fill=BOTH, expand=1, anchor=N)

    api_list_box = Listbox(master=listbox_frame, selectmode=SINGLE, height=len(core_main.apis))
    api_list_box.pack(side=LEFT, expand=1, fill=BOTH, anchor=N)
    api_list_box.bind("<Button-3>", api_listbox_context_menu_popup_event)

    api_list_box.bind("<Double-Button-1>", lambda event: open_api_config(core_main))

    api_status_list_box = Listbox(master=listbox_frame, selectmode=SINGLE)
    api_status_list_box.pack(side=LEFT, expand=1, fill=BOTH)

    update_statuses()

    api_scrollbar = Scrollbar(master=listbox_frame, orient=VERTICAL,
                              command=lambda *args: (api_list_box.yview(*args), api_status_list_box.yview(*args)))

    api_list_box.config(yscrollcommand=api_scrollbar.set)
    api_status_list_box.config(yscrollcommand=api_scrollbar.set)

    api_list_box.bind("<MouseWheel>", mouse_wheel)
    api_status_list_box.bind("<MouseWheel>", mouse_wheel)

    api_scrollbar.pack(side=LEFT, fill=Y)

    analytics_frame = LabelFrame(master=bottom_paned_window, relief=GROOVE, borderwidth=5, text="Analytics")
    # weather_frame.pack(side=BOTTOM, expand=1, fill=BOTH, anchor=S)
    bottom_paned_window.add(analytics_frame)

    analytics_frame_notebook = Notebook(master=analytics_frame)
    analytics_frame_notebook.pack(fill=BOTH, expand=1)

    weather_notebook = Notebook(master=analytics_frame_notebook)  # .pack(expand=1, fill=BOTH)
    analytics_frame_notebook.add(weather_notebook, text="Weather")

    c = Canvas(master=analytics_frame_notebook, bg="yellow")  # .pack(expand=1, fill=BOTH)
    analytics_frame_notebook.add(c, text="Astronomy")

    c = Canvas(master=analytics_frame_notebook, bg="green")  # .pack(expand=1, fill=BOTH)
    analytics_frame_notebook.add(c, text="Warnings")

    mainloop(core_main)


def update_statuses():
    api_list_box.delete(0, END)
    api_status_list_box.delete(0, END)
    for api in CORE_MAIN.apis:
        api_list_box.insert(END, api.NAME)
        api_status_list_box.insert(END, api_constants.statuses[api.get_status()])


def api_listbox_context_menu_popup_event(event):
    if api_list_box.curselection():
        selected_api = CORE_MAIN.apis[api_list_box.curselection()[0]]
    else:
        return

    menu = Menu(master=api_list_box, tearoff=0)
    menu.add_command(label=selected_api.NAME)
    menu.add_separator()
    menu.add_command(label="Update statuses", command=update_statuses)
    menu.add_command(label="Open config", command=selected_api.config)
    menu.post(event.x_root, event.y_root)
    api_list_box.focus()


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
latitude_entry: Entry
longitude_entry: Entry
theme_var: StringVar
THEME: str = "none"
CORE_MAIN = None
api_status_list_box: Listbox
