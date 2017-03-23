from Tkinter import *
import os
import HexagonGame
def startGame(numRing, radius):
    path = "images/" + selectedImage
    hexGame = HexagonGame.HexagonGame(numRing, path, radius)
    hexGame.startGame()
project_root = Tk()
project_root.title("Team 6 Hexagonal Puzzle Game")
project_root.minsize(500,500)
project_root.configure(bg='lightblue')

intro = "1. Select Image You Wish To Use For The Game.\n"
intro += "2. Then Press START!"

Label(project_root, text=intro, pady=10, justify=LEFT, bg='lightblue').grid(row=0, column=0,columnspan=3, sticky=W)

#Select Image from Game
Label(project_root, text="Select Image", bg='lightblue').grid(row=1, column=0, sticky=W)

image_button = Menubutton(project_root, text='Image', relief='raised', padx=2, pady=2)
image_button.grid(row=1, column=1, sticky=W)

image_indicator = Label(project_root, text="Image: None", bg="gold", width=40)
image_indicator.grid(row=1, column=2, columnspan=2)

image_menu = Menu(image_button, tearoff=1)
global selectedImage
def update_image(image):
    global default_image
    global selectedImage
    image_indicator.configure(text=image)
    selectedImage = image
    print "You selected %s" % image

imageFiles = os.listdir("images")
for image in imageFiles:
    image_menu.add_command(label=image, command=lambda image=image: update_image(image))
image_button.configure(menu=image_menu)


start_button3Ring = Button(project_root, text="START with 3 Rings", command=lambda: startGame(3, 70))
start_button3Ring.grid(row=5, column=3)

start_button2Ring = Button(project_root, text="START with 2 Rings", command=lambda: startGame(2, 110))
start_button2Ring.grid(row=5, column=2)

quit_button = Button(project_root, text='QUIT', command=quit)
quit_button.grid(row=6, column=0, sticky=W, pady=4)

project_root.mainloop()
