from Tkinter import *

def getImgName():
    return ['Test1','Test2']

def start():
    pass
master = Tk()
master.title("Menu")
canvas = Canvas(master, width=300, height=500)
canvas.grid(row=0, column=0, rowspan=5)

title = Label(master, text="HexagonGame")
title.grid(row=0, column=0)

ring = StringVar(master)
ring.set("two")  # initial value
ringSelect = OptionMenu(master, ring, "two", "three")
ringSelect.grid(row=1, column=0)

imgName = StringVar(master)
imgName.set("Test1")  # initial value
imgSelect = OptionMenu(master, imgName, *getImgName())
imgSelect.grid(row=2, column=0)

canvas = Canvas(master, width=100, height=100)
canvas.create_rectangle(0, 0, 100, 100, fill="blue")
canvas.grid(row=3, column=0)

start = Button(master, text="Start", command=start)
start.grid(row=4, column=0)

master.mainloop()

