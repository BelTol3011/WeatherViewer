print("[Launch] preloading GUI")

from GUI import Main as GuiMain

print("[Launch] ... finished!")

import Core.Main as CoreMain

GuiMain.start(CoreMain)
