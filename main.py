from tkinter import Tk
from system import System, Data, TitleBottom





root = Tk()
root.title("飲料價格查詢系統")
root.minsize(width=700,height=900)
root.configure(background="white")



bigfont = ("LingWai TC",15)
root.option_add("*TCombobox*Listbox*Font", bigfont)

data = Data()
title = TitleBottom(root)
system = System(root,data)


root.mainloop()
