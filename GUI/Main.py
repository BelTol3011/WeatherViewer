from tkinter import *


def mainloop():
    if not root:
        raise Exception("[GUI] No main Window created.")

    while 1:
        root.update()


def start():
    global root

    root = Tk()
    root.title("WeatherViewer by JHondah and Belissimo")
    print(type(root))
    mainloop()


root: Tk
