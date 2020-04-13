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
    global root, search_bar

    root = Tk()
    root.title("WeatherViewer by JHondah and Belissimo")
    
    search_bar = Entry(master=root)
    search_bar.pack(side=TOP, pady=10)
    
    mainloop()


root: Tk
search_bar: Entry
