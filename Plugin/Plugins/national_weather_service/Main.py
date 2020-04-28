from tkinter import *
import Plugin.API_constants as api_constants

NAME = "National Weather Service (USA)"
CONFIGURE = lambda: Tk().mainloop()

def get_status():
    return api_constants.INACTIVE