from tkinter import *


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
                raise Exception(f"[GUI] Maximum error count of {max_errors} exceeded, terminating.")


def start():
    global root

    root = Tk()
    root.title("WeatherViewer by JHondah and Belissimo")
    print(type(root))

    mainloop()


root: Tk
