print("[Launch] preloading GUI")
import GUI.Main as GuiMain

print("[Launch] ... finished!")

import Core.Main as CoreMain

GuiMain.start(CoreMain)
