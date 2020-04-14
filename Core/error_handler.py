import tkinter.messagebox

mode = "User"


def error(error):
    if mode == "User":
        o = tkinter.messagebox.askyesno("An Error occurred!",
                                        "Error:\n" + str(error) + "\nDo you want to ignore this error?")
        if not o:
            raise Exception("Look at the above exception!, " + str(error))
    else:
        raise Exception(error)
