from tkinter import *
from ttk import *
import Core.error_handler as eh
import API.API_constants as api_constants
from ttkthemes import themed_tk
from typing import List, Tuple
import copy
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler


def quit():
    global _mainloop
    print("[GUI] Window close button event, terminating. Ignore any GUI-errors that follow.")
    _mainloop = False
    root.destroy()


def mainloop():
    global city, selected, prevtext
    if not root:
        raise eh.error("[GUI] No main Window created yet.")

    def set_city(event: EventType):
        global selected, city, prevtext
        widget: Listbox = event.widget
        city_index = widget.curselection()[0]
        widget_index = 0
        for database in search_listboxes:
            if database[1] == widget:
                break
            widget_index += 1
        city = data[widget_index][city_index]
        prevtext = search_listboxes[widget_index][0].format(city)
        search_bar.delete(0, END)
        search_bar.insert(0, prevtext)
        print(city)
        selected = 1

    for database in search_listboxes:
        database[1].bind("<Double-Button-1>", set_city)

    error_count = 0
    max_errors = 10
    prevtext = search_bar.get()
    selected = False
    data = []

    while _mainloop:
        try:
            root.update()
            text = search_bar.get()

            if (text != prevtext) and (text != ""):
                selected = False
                prevtext = text
                city = city_none
                search_list_box_frame.pack(fill=BOTH, expand=1)
                data = []
                for database in search_listboxes:
                    latitude_entry.config(state=NORMAL)
                    longitude_entry.config(state=NORMAL)
                    latitude_entry.delete(0, END)
                    longitude_entry.delete(0, END)

                    status_bar.config(text="Searching cities...")
                    root.update()
                    database[1].delete(0, END)
                    search_list = database[0].search_city_list(text)
                    elements = [database[0].format(city) for city in search_list]
                    data.append(search_list)
                    database[1].insert(0, *elements)
                    database[1].config(height=len(elements))
                    status_bar.config(text="Ready...")
            elif (text == "") and (not selected):
                search_list_box_frame.pack_forget()

            if selected == 1:

                latitude_entry.delete(0, END)
                longitude_entry.delete(0, END)
                latitude_entry.insert(0, city["coord"]["lat"])
                longitude_entry.insert(0, city["coord"]["lon"])
                latitude_entry.config(state=DISABLED)
                longitude_entry.config(state=DISABLED)
            elif selected == 2:
                search_bar.delete(0, END)
                search_bar.config(state=DISABLED)
            else:
                search_bar.config(state=NORMAL)
                latitude_entry.config(state=NORMAL)
                longitude_entry.config(state=NORMAL)

            if latitude_entry.get() and longitude_entry.get() and (selected != 1):
                selected = 2
                city = copy.deepcopy(city_none)
                city["coord"].update({"lat": latitude_entry.get(), "lon": longitude_entry.get()})
            elif (latitude_entry.get() or longitude_entry.get()) and (selected == 2):
                selected = False
                search_bar.config(state=NORMAL)

            if selected:
                search_list_box_frame.pack_forget()
                select_city_info_label.config(text="Area selected.")
            else:
                select_city_info_label.config(text="Or enter latitude and longitude of you location.")
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
    core_main.api_plugins[api_list_box.curselection()[0]].config()


def start(core_main):
    def mouse_wheel(event):
        scroll = round(event.delta / 60) * -1
        api_list_box.yview("scroll", scroll, "units")
        api_status_list_box.yview("scroll", scroll, "units")
        return "break"

    global root, search_bar, menu_bar, api_list_box, search_list_box_frame, status_bar, search_listboxes, \
        select_city_info_label, latitude_entry, longitude_entry, theme_var, CORE_MAIN, api_status_list_box
    CORE_MAIN = core_main
    root = themed_tk.ThemedTk(theme=THEME)
    root.title("WeatherViewer by JHondah and Belissimo")
    root.protocol("WM_DELETE_WINDOW", quit)

    menu_bar = Menu(master=root)
    # MENU CONFIGURATION -------------------------------------------------------
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Settings")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # edit_menu = Menu(menu_bar, tearoff=0)
    # edit_menu.add_radiobutton(label="Germany")
    # edit_menu.add_radiobutton(label="UK/USA")
    # edit_menu.invoke(0)
    # menu_bar.add_cascade(label="Localization", menu=edit_menu)

    api_menu = Menu(menu_bar, tearoff=0)
    for plugin in core_main.plugins:
        api_menu.add_command(label=plugin.name, command=plugin.config)
    menu_bar.add_cascade(label="Plugins", menu=api_menu)

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

    # MENU CONFIGURATION PAUSE ----------------------------------------------------------------

    status_bar = Label(master=root, text="Ready...", anchor=W)
    status_bar.pack(fill=X, side=BOTTOM)

    bottom_paned_window = PanedWindow(master=root, orient=VERTICAL)
    bottom_paned_window.pack(fill=BOTH, expand=1)

    main_paned_window = PanedWindow(master=bottom_paned_window, orient=HORIZONTAL)
    bottom_paned_window.add(main_paned_window)

    select_city_frame = LabelFrame(master=main_paned_window, relief=GROOVE, borderwidth=5, text="Area Selection")
    # select_city_frame.pack(fill=X, side=LEFT, anchor=N, expand=1)

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
    search_listboxes = []

    for plugin in [plugin for plugin in core_main.plugins if plugin.search_city_list]:
        print("add")
        search_list_box = Listbox(master=search_list_box_frame)
        search_list_box.pack(fill=BOTH, expand=1, anchor=N, side=LEFT)
        search_scrollbar = Scrollbar(master=search_list_box_frame, command=search_list_box.yview)
        search_list_box.config(yscrollcommand=search_scrollbar.set)
        search_scrollbar.pack(side=LEFT, anchor=N, fill=Y)
        search_listboxes.append((plugin, search_list_box))

    apis_frame = LabelFrame(master=main_paned_window, relief=GROOVE, borderwidth=5, text="API Manager", labelanchor=N)
    # apis_frame.pack(fill=X, side=RIGHT, anchor=N)
    # main_paned_window.add(apis_frame)

    apis_text_frame = Frame(master=apis_frame)
    apis_text_frame.pack(fill=X, side=TOP, anchor=N, expand=1)

    Label(master=apis_text_frame, text="APIs:").pack(fill=X, side=LEFT, expand=1)
    Label(master=apis_text_frame, text="Statuses:").pack(fill=X, side=LEFT, expand=1)

    listbox_frame = Frame(master=apis_frame)
    listbox_frame.pack(side=TOP, fill=BOTH, expand=1, anchor=N)

    api_list_box = Listbox(master=listbox_frame, selectmode=SINGLE, height=len(core_main.api_plugins))
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

    weather_frame = Frame(master=analytics_frame_notebook)  # .pack(expand=1, fill=BOTH)
    analytics_frame_notebook.add(weather_frame, text="Weather")

    matplotlib_cavas_weather_frame = Frame(master=weather_frame)
    matplotlib_cavas_weather_frame.pack(fill=BOTH, expand=1)

    figure = core_main.get_matplotlib_figure_weather()

    canvas = FigureCanvasTkAgg(figure, master=matplotlib_cavas_weather_frame)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, matplotlib_cavas_weather_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def on_key_press(event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect("key_press_event", on_key_press)

    c = Canvas(master=analytics_frame_notebook, bg="yellow")  # .pack(expand=1, fill=BOTH)
    analytics_frame_notebook.add(c, text="Astronomy")

    c = Canvas(master=analytics_frame_notebook, bg="green")  # .pack(expand=1, fill=BOTH)
    analytics_frame_notebook.add(c, text="Warnings")

    # MENU CONFIGURATION UNPAUSE --------------------------------------------------------------------
    display_menu.add_cascade(label="Themes", menu=themes_menu)
    display_menu.add_separator()
    area_selection_var = IntVar()
    api_manager_var = IntVar()
    analytics_var = IntVar()

    def insert_display_menu_add(child, pos, var, pane_window):
        if var.get():
            dummy = Label(master=pane_window)
            pane_window.add(dummy)
            pane_window.insert(pos, child)
            pane_window.forget(dummy)
        else:
            pane_window.forget(child)

    display_menu.add_checkbutton(label="Area Selection", variable=area_selection_var,
                                 command=lambda: insert_display_menu_add(select_city_frame, 0,
                                                                         area_selection_var, main_paned_window))
    display_menu.add_checkbutton(label="API Manager", variable=api_manager_var,
                                 command=lambda: insert_display_menu_add(apis_frame, END,
                                                                         api_manager_var, main_paned_window))
    display_menu.add_checkbutton(label="Analytics", variable=analytics_var,
                                 command=lambda: insert_display_menu_add(analytics_frame, END,
                                                                         analytics_var, bottom_paned_window))
    # main_paned_window.add(apis_frame)
    display_menu.invoke(2)
    display_menu.invoke(3)
    display_menu.invoke(4)

    # main_paned_window.add(apis_frame)

    menu_bar.add_cascade(label="Display", menu=display_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    menu_bar.add_cascade(label="Help", menu=help_menu)
    # MENU CONFIGURATION END ---------------------------------------------------
    root.config(menu=menu_bar)

    mainloop(core_main)


def update_statuses():
    api_list_box.delete(0, END)
    api_status_list_box.delete(0, END)
    for plugin in CORE_MAIN.api_plugins:
        api_list_box.insert(END, plugin.name)
        api_status_list_box.insert(END, api_constants.statuses[plugin.api.get_status()])


def api_listbox_context_menu_popup_event(event):
    if api_list_box.curselection():
        selected_api = CORE_MAIN.api_plugins[api_list_box.curselection()[0]]
    else:
        return

    menu = Menu(master=api_list_box, tearoff=0)
    menu.add_command(label=selected_api.name)
    menu.add_separator()
    menu.add_command(label="Update statuses", command=update_statuses)
    menu.add_command(label="Open config", command=selected_api.config)
    menu.post(event.x_root, event.y_root)
    api_list_box.focus()


city_none = {"name": "Unknown", "country": "Unknown", "coord": {"lat": None, "lon": None}}
city = city_none
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
CORE_MAIN: object
api_status_list_box: Listbox
search_listboxes: List[Tuple[object, Listbox]]
selected: bool = False
