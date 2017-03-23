from Tkinter import *
import numpy as np
from scipy import misc
from PIL import Image, ImageDraw, ImageTk
import math
import random
import os

class HexagonGame(object):
    def __init__(self, num_rings, img_path, radius):
        self.numRings = num_rings
        self.imgPath = img_path
        self.rings = []
        self.hexIDs = []  # A list of IDs for all your hexagons
        self.removedList = []
        self.boundaryIDs = []
        self.imgIDs = []
        self.images = {}
        self.backgroundsDONTUSE = {}
        self.moving = False
        self.canvas1 = None
        self.label1 = None
        self.r = radius
        self.center = ()
        self.baseMask = self.drawMaskImage()
        self.prevHex = None
        self.fullPic = None
        self.label1 = None
        self.solveStack = []
        self.solveButton = None
        ## Clear the bgImages directory
        if not os.path.exists("bgImages"):
            os.makedirs("bgImages")
        for file in os.listdir("bgImages"):
            os.remove("bgImages/"+file)
        self.run_game()

    # Defining the center point of the puzzle
    def center_point(self, m, n):
        # m equates to the x values of the puzzle
        # n equates to the y values of the puzzle

        # Grabbing the canvas center point (x, y)
        xCenter = self.center[0]
        yCenter = self.center[1]
        CanvasCenter = np.array([xCenter, yCenter])
        # Important note: canvas center is not a graphical center of (0, 0) of the x and y planes

        # Vectors in an array that account for quadrant I and quadrant IV of the unit circle, respectively
        v1 = self.r * np.array([1 + np.cos(np.pi / 3), np.sin(np.pi / 3)])
        v2 = self.r * np.array([1 + np.cos(np.pi / 3), -np.sin(np.pi / 3)])

        # z is going to be all the new centers from the canvas center
        # This is calculated using m and n as well as the unit vectors
        hexCenter = m * v1 + n * v2 + CanvasCenter
        # If m and n are (0, 0) we are on the center of our canvas, our psuedo origin, which is what we want
        return hexCenter

    def draw_hexagons(self):
        # for loops to iterate over values in the x plane, or m, and in the y plane, or n
        for m in range(-4, 5):
            for n in range(-4, 5):
                # Setting base colour and outline for hexagons
                colour = "green"
                outline = "black"

                # Setting the created hexagon's center point
                hexCenter = self.center_point(m, n)

                # Grabbing the canvas center point (x, y)
                xCenter = self.center[0]
                yCenter = self.center[1]
                CanvasCenter = np.array([xCenter, yCenter])

                # Determining which ring the created hexagon falls into: 1, 2, or 3 if making 3 rings
                # Calculates the magnitude of the vector between center point of the created hexagon and canvas center
                # Divides the distance by the radius of the circle enclosing the hexagons
                # Given distance determines the ring that the hexagon is on
                ring_radius = np.linalg.norm(hexCenter - CanvasCenter) / self.r
                ring_radius = round(ring_radius, 5)

                # Ring 1 falling on 1.732...
                if 0 < ring_radius < 2:
                    ring_number = 1
                    colour = "magenta"

                # Ring 2 falling on 3.000... or 3.464...
                elif 2 < ring_radius < 4:
                    ring_number = 2
                    colour = "purple"

                # Potential ring 3 falling on 4.582... or 5.196...
                elif self.numRings == 3:
                    if 4 < ring_radius < 6:
                        ring_number = 3
                        colour = "cyan"
                    else:
                        ring_number = 100
                        colour = ""

                # All other rings past 3
                else:
                    ring_number = 100
                    colour = ""

                # Accounting for the center hexagon at (0, 0) or at canvas (500, 500)
                if ring_radius == 0.0:
                    ring_number = 100

                # Appending the list of rings in order of when its made
                self.rings.append(ring_radius)

                # Creating empty list of the center points for the rings
                points = []

                if ring_radius < 6:
                    for k in range(6):
                        # Setting up creation of 6 points forming hexagon shape

                        x, y = hexCenter[0] + self.r * np.cos(k * np.pi / 3), hexCenter[1] + self.r * np.sin(k * np.pi / 3)
                        # Point (x, y) from hexagon radius to create the  points from its designated center point
                        points.extend([x, y])
                        # Extending it all into a list

                    # Connecting all points together forming the hexagon and giving it a hexagon identification number
                    newHexID = self.canvas1.create_polygon(points, activefill="yellow", fill="",outline=outline, width=3)
                    self.hexIDs.append(newHexID)
                    # Appending hexagon identification into a list
                    # Calling a method with image name from mask and adding it as a tag
                    # Placeholder for the time being

                    # Adding tags to each hexagon: Identification, Ring Number, x Center Value, y Center Value
                    self.canvas1.itemconfig(newHexID, tags=(newHexID, str(ring_number), int(round(hexCenter[0])),
                                                            int(round(hexCenter[1])), int(round(hexCenter[0])),
                                                                      int(round(hexCenter[1]))))

        # Deleting the center hexagon that has been tagged with "100" using a for loop and getting tags
        # These include rings outside of 2, or 3 if its included, and the center
        removedList = []
        for hex in self.hexIDs:
            if int(self.canvas1.gettags(hex)[1]) == 100:
                self.canvas1.delete(hex)
                self.removedList.append(hex)
        for item in self.removedList:
            self.hexIDs.remove(item)

        self.boundary()

    def boundary(self):
        for m in range(-4, 5):
            for n in range(-4, 5):
                colour = ""
                outline = ""

                hexCenter = self.center_point(m, n)

                # Grabbing the canvas center point (x, y)
                xCenter = self.center[0]
                yCenter = self.center[1]
                CanvasCenter = np.array([xCenter, yCenter])

                # Hexagons will fall onto ring 4, a boundry ring for movement
                # Calculates the magnitude of the vector between center point of the created hexagon and canvas center
                # Divides the distance by the radius of the circle enclosing the hexagons
                # Given distance determines the ring that the hexagon is on
                ring_radius = np.linalg.norm(hexCenter - CanvasCenter) / self.r
                ring_radius = round(ring_radius, 5)

                pointsB = []

                if self.numRings == 2:
                    if 4.0 < ring_radius < 5.5:
                        for k in range(6):
                            # Setting up creation of 6 points forming hexagon shape

                            x, y = hexCenter[0] + self.r * np.cos(k * np.pi / 3), hexCenter[1] + self.r * np.sin(
                                k * np.pi / 3)
                            # Point (x, y) from hexagon radius to create the  points from its designated center point
                            pointsB.extend([x, y])
                            # Extending it all into a list

                        # Connecting all points together forming the hexagon and giving it a hexagon identification number
                        newBoundaryID = self.canvas1.create_polygon(pointsB, fill=colour, outline=outline,
                                                                    width=3)
                        self.boundaryIDs.append(newBoundaryID)
                        # Appending hexagon identification into a list
                        # Calling a method with image name from mask and adding it as a tag
                        # Placeholder for the time being

                        # Adding tags to each hexagon: Identification, Ring Number, x Center Value, y Center Value
                        self.canvas1.itemconfig(newBoundaryID, tags=(newBoundaryID, ring_radius))

                if self.numRings == 3:
                    if 5.5 < ring_radius < 7:

                        for k in range(6):
                            # Setting up creation of 6 points forming hexagon shape

                            x, y = hexCenter[0] + self.r * np.cos(k * np.pi / 3), hexCenter[1] + self.r * np.sin(
                                k * np.pi / 3)
                            # Point (x, y) from hexagon radius to create the  points from its designated center point
                            pointsB.extend([x, y])
                            # Extending it all into a list

                        # Connecting all points together forming the hexagon and giving it a hexagon identification number
                        newBoundaryID = self.canvas1.create_polygon(pointsB, fill=colour, outline=outline,
                                                                    width=3)
                        self.boundaryIDs.append(newBoundaryID)
                        # Appending hexagon identification into a list
                        # Calling a method with image name from mask and adding it as a tag
                        # Placeholder for the time being

                        # Adding tags to each hexagon: Identification, Ring Number, x Center Value, y Center Value
                        self.canvas1.itemconfig(newBoundaryID, tags=(newBoundaryID, ring_radius))

    ################################################## Image Masking ##################################################
    def maskImage(self, imgToMask):
        if imgToMask.mode == "RGB":
            imgToMask = np.array(imgToMask.getdata()).reshape(imgToMask.size[0], imgToMask.size[1], 3)
        else:
            imgToMask = np.array(imgToMask.getdata()).reshape(imgToMask.size[0], imgToMask.size[1], 4)

        row, col, z = imgToMask.shape
        # Getting base image data to create the mask
        mask = np.array(self.baseMask.getdata()).reshape(self.baseMask.size[0], self.baseMask.size[1], 3)

        # Creating the mask
        mask = np.dstack((mask, np.full((row, col), 255)))
        if z == 3:
            imgToMask = np.dstack((imgToMask, np.full((row, col), 255)))
        for r in range(0, row):
            for c in range(0, col):
                if np.all(mask[r][c] == [0, 0, 0, 255]):
                    mask[r][c] = (0, 0, 0, 0)
                else:
                    mask[r][c] = (1, 1, 1, 1)

        # Mask the image and save it
        maskedImage = np.ma.masked_array(imgToMask, mask=mask)
        maskedImage = maskedImage.filled([0, 0, 0, 0])
        imageName = "bgImages/img" + str(random.randint(0, 1000)) + ".png"
        while imageName in os.listdir("bgImages"):
            imageName = "bgImages/img" + str(random.randint(0, 1000)) + ".png"
        misc.imsave(imageName, maskedImage)
        return imageName

    # Returns the points on a hexagon centered at 50, 50 for this demo
    def hexagonPoints(self, imageSize):
        points = []
        for k in range(6):
            x, y = imageSize/2.0 + self.r * np.cos(k * np.pi / 3), imageSize/2.0 + self.r * np.sin(k * np.pi / 3)
            points.extend([x, y])
        return points

    # Creates the image to use as the mask.
    # This image is never saved as it is passed as a parameter to maskImage
    def drawMaskImage(self):
        image2 = Image.new('RGB', (self.r*2, self.r*2), 'white')
        draw = ImageDraw.Draw(image2)
        hexagon = self.hexagonPoints(self.r*2)
        draw.polygon(hexagon, fill='black')
        return image2

    def sliceBackground(self, x, y):
        bg = Image.open(self.imgPath).copy()
        left = x - self.r
        upper = y - self.r
        right = x + self.r
        lower = y + self.r
        cropBox = (left, upper, right, lower)
        return self.maskImage(bg.crop(cropBox))
    ###################################################################################################################

    def getAllCurrentCenterPoints(self, getBoundary):
        listCenPoints = []
        for hex in self.hexIDs:
            center = self.canvas1.coords(hex)[:2]
            center[0] = center[0] - self.r
            center[0] , center[1] = int(round(center[0])) , int(round(center[1]))
            listCenPoints.append(center)
        if getBoundary:
            for hex in self.boundaryIDs:
                center = self.canvas1.coords(hex)[:2]
                center[0] = center[0] - self.r
                center[0] , center[1] = int(round(center[0])) , int(round(center[1]))
                listCenPoints.append(center)
        return listCenPoints
    # Defining a method that registers mouse clicks and changes hexagon colour to red
    def click(self, event):
        if self.canvas1.find_withtag(CURRENT):
            if int(self.canvas1.gettags(CURRENT)[0]) in self.boundaryIDs or self.moving:
                return
            # CURRENT takes in all the tags from the currently clicked hexagon tile
            hexId = self.canvas1.gettags(CURRENT)[0]
            moveToMake = self.getMoves(hexId)
            self.moveTile(hexId, moveToMake, 0)
            self.canvas1.update()
            self.solveStack.append(hexId)


    def getMoves(self,hexId):
        # Picks the correct move
        # The moves are set up in the clock face
        centerpoint = self.canvas1.coords(hexId)[:2]
        centerpoint[0] = centerpoint[0] - self.r
        clockposition = -1
        CurrentCenterPoints = self.getAllCurrentCenterPoints(True)
        for i in range(0,6,1):
            checkpoint = [centerpoint[0] + math.sqrt(3)*self.r*math.cos(math.radians(30 + 60*i)), centerpoint[1] + math.sqrt(3)*self.r*math.sin(math.radians(30 + 60*i))]
            checkpoint[0] , checkpoint[1] = int(round(checkpoint[0])), int(round(checkpoint[1]))
            if not checkpoint in CurrentCenterPoints:
                clockposition = i
        clock1200 = [0.0, -np.sqrt(3) * self.r]
        clock0600 = [0.0, +np.sqrt(3) * self.r]
        clock0200 = [3.0 * self.r / 2.0, -np.sqrt(3) * self.r / 2.0]
        clock0400 = [3.0 * self.r / 2.0, +np.sqrt(3) * self.r / 2.0]
        clock1000 = [-3.0 * self.r / 2.0, -np.sqrt(3) * self.r / 2.0]
        clock0800 = [-3.0 * self.r / 2.0, +np.sqrt(3) * self.r / 2.0]

        positions = {}
        positions[3] = clock1000
        positions[4] = clock1200
        positions[5] = clock0200
        positions[0] = clock0400
        positions[1] = clock0600
        positions[2] = clock0800
        if clockposition == -1:
            return False
        return positions[clockposition]
        # dx, dy = random.choice(direction)  # Total move to perform.
        # self.canvas1.move(self.hexID, dx, dy)

    def moveTile(self, hexId, moveToMake, n):
        if moveToMake == False:
            return
        dx, dy = moveToMake
        self.moving = True
        if n < 10:
            deltax = dx / 10.0;
            deltay = dy / 10.0  # Break up the move into 20 small steps for the animation.
            self.canvas1.move(hexId, deltax, deltay)
            imgId = self.images[int(hexId)]
            self.canvas1.move(imgId, deltax, deltay)
            self.root.after(20, self.moveTile, hexId, moveToMake, n + 1)
        if n == 10:
            self.moving = False
            self.checkWin()
            return
    def scramble(self, n):
        if self.numRings == 3:
            numRand = 20
        elif self.numRings == 2:
            numRand = 10
        if n < numRand:
            potentialMoves = {}
            for hex in self.hexIDs:
                move = self.getMoves(hex)
                if move:
                    potentialMoves[hex] = move
            selectedHex = random.choice(potentialMoves.keys())
            while selectedHex == self.prevHex:
                selectedHex = random.choice(potentialMoves.keys())
            self.prevHex = selectedHex
            self.moveTile(selectedHex, potentialMoves[selectedHex], 0)
            self.solveStack.append(selectedHex)
            self.root.after(400, self.scramble, n + 1)

    def checkWin(self):
        won = True
        for hex in self.hexIDs:
            currCenter = self.canvas1.coords(hex)[:2]
            currCenter[0] = currCenter[0] - self.r
            currX, currY = int(round(currCenter[0])), int(round(currCenter[1]))
            correctX, correctY = int(self.canvas1.gettags(hex)[2]), int(self.canvas1.gettags(hex)[3])
            if correctX != currX or correctY != currY:
                won = False
        if won == True:
            for hex in self.hexIDs:
                self.canvas1.delete(hex)
            for hex in self.boundaryIDs:
                self.canvas1.delete(hex)
            for imgId in self.imgIDs:
                self.canvas1.delete(imgId)
            self.canvas1.create_image(500, 500, image=self.fullPic)
            self.label1.destroy()
            self.solveButton.destroy()
            Button(self.root,text="Quit", command=quit).grid(row=1, column=0)

    def solve(self, n):
        if n < len(self.solveStack):
            hex = self.solveStack.pop()
            move = self.getMoves(hex)
            self.moveTile(hex,move,0)
            self.root.after(400, self.solve, n)
            self.checkWin()
    # Defining a method that starts the game
    def run_game(self):
        # Standard Tkinter stuff
        root = Toplevel()
        root.title("Hexagon Puzzle Game!")
        self.root = root
        Tk.title = "Making Board Game"

        # Creating the canvas for the game
        canvas1 = Canvas(self.root, width=1000, height=1000, bg="white", highlightthickness=0, bd=0)
        canvas1.grid(row=0, column=0)
        self.label1 = Label(self.root, text="Move mouse over hexagons and click them")
        self.label1.grid_configure(row=1, column=0)
        self.solveButton = Button(self.root, text="Solve", command=lambda: self.solve(0))
        self.solveButton.grid(row=1, column=1)
        self.canvas1 = canvas1
        self.canvas1.bind('<ButtonPress-1>', self.click)

        # Getting center of canvas and setting it
        width = eval(canvas1["width"])
        height = eval(canvas1["height"])
        self.center = (width/2, height/2)

        # Calls method draw_hexagons() to draw in the hexagons
        self.draw_hexagons()
        for hex in self.hexIDs:
            x = int(self.canvas1.gettags(hex)[2])
            y = int(self.canvas1.gettags(hex)[3])
            hexBG = ImageTk.PhotoImage(file = self.sliceBackground(x, y))
            imgId = self.canvas1.create_image(x, y, image=hexBG)
            self.imgIDs.append(imgId)
            self.backgroundsDONTUSE[hex] = hexBG
            self.images[hex] = imgId
            self.canvas1.tag_raise(hex)
            root.update()
        self.scramble(0)
        self.fullPic = ImageTk.PhotoImage(file=self.imgPath)
        # tiles moving etc etc

        self.root.mainloop()

