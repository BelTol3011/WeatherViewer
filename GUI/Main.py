from tkinter import *
import Core.error_handler as eh


def mainloop():
    if not root:
        raise Exception("[GUI] No main Window created.")

    error_count = 0
    max_errors = 10
    while 1:
        try:
            root.update()
        except TclError as e:
            print("[GUI] TclError occurred:", e)
            error_count += 1
            if error_count >= max_errors:
                eh.error(f"[GUI] Maximum error count of {max_errors} exceeded, terminating.")


def start():
    global root, search_bar, text_label, menu_bar
    root = Tk()
    root.title("WeatherViewer by JHondah and Belissimo")

    menu_bar = Menu(master=root)
    # MENU CONFIGURATION -------------------------------------------------------
    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.destroy)
    menu_bar.add_cascade(label="File", menu=file_menu)

    edit_menu = Menu(menu_bar, tearoff=0)
    edit_menu.add_radiobutton(label="Germany")
    edit_menu.add_radiobutton(label="UK/USA")
    edit_menu.invoke(0)
    menu_bar.add_cascade(label="Localization", menu=edit_menu)

    api_menu = Menu(menu_bar, tearoff=0)
    api_menu.add_command(label="OpenWeatherMap")
    menu_bar.add_cascade(label="APIs", menu=api_menu)

    help_menu = Menu(menu_bar, tearoff=0)
    help_menu.add_command(label="About")
    menu_bar.add_cascade(label="Help", menu=help_menu)
    # MENU CONFIGURATION END ---------------------------------------------------
    root.config(menu=menu_bar)

    text_label = Label(master=root, text="Type the name of the city you want to have the weather data of:",
                       justify=CENTER)
    text_label.pack(side=TOP, pady=10, fill=BOTH, padx=10)

    search_bar = Entry(master=root)
    search_bar.pack(side=TOP, pady=5, fill=BOTH, padx=10)

    mainloop()


root: Tk
search_bar: Entry
text_label: Label
menu_bar: Menu
