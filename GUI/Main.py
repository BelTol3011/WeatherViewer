from tkinter import *
import Core.error_handler as eh


def quit():
    global _mainloop
    print("[GUI] Window close button event, terminating.")
    _mainloop = False
    root.destroy()


def mainloop():
    if not root:
        raise Exception("[GUI] No main Window created.")

    error_count = 0
    max_errors = 10
    while _mainloop:
        try:
            root.update()
        except TclError as e:
            print("[GUI] TclError occurred:", e)
            error_count += 1
            if error_count >= max_errors:
                eh.error(f"[GUI] Maximum error count of {max_errors} exceeded, terminating.")


def open_api_config(core_main):
    core_main.apis[api_list_box.curselection()[0]].config()


def start(core_main):
    global root, search_bar, menu_bar, api_list_box
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

    all_frame = Frame(master=root)
    all_frame.pack(side=TOP, expand=1, fill=BOTH)

    select_city_frame = Frame(master=all_frame)
    select_city_frame.pack(fill=X, side=LEFT, expand=1, anchor=N)

    Label(master=select_city_frame, text="Type the name of the city you want to have the weather data of:",
          justify=LEFT, anchor=W).pack(side=TOP, pady=10, fill=BOTH, padx=10)

    search_bar = Entry(master=select_city_frame)
    search_bar.pack(side=TOP, pady=5, fill=BOTH, padx=10)

    apis_frame = Frame(master=all_frame, relief=RIDGE, borderwidth=5)
    apis_frame.pack(fill=BOTH, side=RIGHT, anchor=N)

    Label(master=apis_frame, text="APIs:").pack(fill=X)

    listbox_frame = Frame(master=apis_frame)
    listbox_frame.pack(side=TOP, fill=BOTH, expand=1)

    api_list_box = Listbox(master=listbox_frame, selectmode=SINGLE)
    api_list_box.pack(side=LEFT, expand=1, fill=BOTH)
    for api in core_main.apis:
        api_list_box.insert(END, api.NAME)
    api_list_box.itemconfig(0)
    api_list_box.bind("<Double-Button-1>", lambda event: open_api_config(core_main))

    api_scrollbar = Scrollbar(master=listbox_frame, orient=VERTICAL, command=api_list_box.yview)
    api_list_box.config(yscrollcommand=api_scrollbar.set)
    api_scrollbar.pack(side=LEFT, fill=Y)
    # canvas = Canvas(master=apis_frame, bg="red")
    # canvas.pack(pady=10, padx=10)

    mainloop()


root: Tk
search_bar: Entry
menu_bar: Menu
_mainloop = True
api_list_box: Listbox
