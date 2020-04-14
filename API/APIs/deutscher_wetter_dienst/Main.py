from tkinter import *
import API.API_constants as api_constants

NAME = "Deutscher Wetterdienst"
CONFIG = lambda: Tk().mainloop()

def get_status():
    return api_constants.INACTIVE