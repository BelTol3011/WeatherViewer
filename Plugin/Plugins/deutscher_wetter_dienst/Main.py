from tkinter import *
import Plugin.API_constants as api_constants

NAME = "Deutscher Wetterdienst"
CONFIGURE = lambda: Tk().mainloop()

def get_status():
    return api_constants.INACTIVE