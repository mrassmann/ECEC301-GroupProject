from Tkinter import *
import numpy as np
from scipy import misc
from PIL import Image, ImageDraw

class HexagonGame(object):
    def __init__(self, num_rings, img_path):
        self.numRings = num_rings
        self.imgPath = img_path
        self.rings = []
        self.hexIDs = []  # A list of IDs for all your hexagons
        self.canvas1 = None
        self.label1 = None
        self.r = 50
        self.center = ()
        self.baseMask = self.drawMaskImage()
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
                    newHexID = self.canvas1.create_polygon(points, activefill="yellow", fill=colour, outline=outline, width=1)
                    self.hexIDs.append(newHexID)
                    # Appending hexagon identification into a list
                    # Calling a method with image name from mask and adding it as a tag
                    # Placeholder for the time being

                    # Adding tags to each hexagon: Identification, Ring Number, x Center Value, y Center Value
                    self.canvas1.itemconfig(newHexID, tags=(newHexID, str(ring_number), hexCenter[0], hexCenter[1]))

        # Deleting the center hexagon that has been tagged with "100" using a for loop and getting tags
        # These include rings outside of 2, or 3 if its included, and the center
        removedList = []
        for hex in self.hexIDs:
            if int(self.canvas1.gettags(hex)[1]) == 100:
                self.canvas1.delete(hex)
                removedList.append(hex)
        for item in removedList:
            self.hexIDs.remove(item)

    ################################ Image Masking #################################
    def maskImage(self, imgToMask):
        row, col, z = imgToMask.shape
        # Getting base image data to create the mask
        mask = np.array(self.baseMask.getdata()).reshape(self.baseMask.size[0], self.baseMask.size[1], 3)

        # Creating the mask
        if z == 3:
            imgToMask = np.dstack((imgToMask, np.full((row, col), 255)))
            mask = np.dstack((mask, np.full((row, col), 255)))
        for r in range(0, row):
            for c in range(0, col):
                if np.all(mask[r][c] == [0, 0, 0, 255]):
                    mask[r][c] = (0, 0, 0, 0)
                else:
                    mask[r][c] = (1, 1, 1, 1)
        print mask

        # Mask the image and save it
        maskedImage = np.ma.masked_array(imgToMask, mask=mask)
        maskedImage = maskedImage.filled([0, 0, 0, 0])
        misc.toimage(maskedImage, cmin=0.0, cmax=256.0).save('outfile.png')

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
        self.maskImage(bg.crop(cropBox))

    # Defining a method that registers mouse clicks and changes hexagon colour to red
    def click(self, event):
        if self.canvas1.find_withtag(CURRENT):
            # CURRENT takes in all the tags from the currently clicked hexagon tile
            colour = "red"
            self.canvas1.itemconfig(CURRENT, fill=colour)
            self.canvas1.update()

    # Defining a method that starts the game
    def run_game(self):
        # Standard Tkinter stuff
        root = Tk()
        Tk.title = "Making Board Game"

        # Creating the canvas for the game
        canvas1 = Canvas(root, width=1000, height=1000, bg="white", highlightthickness=0, bd=0)
        canvas1.grid(row=0, column=0)
        label1 = Label(root, text="Move mouse over hexagons and click them")
        label1.grid_configure(row=1, column=0)
        self.canvas1 = canvas1
        self.canvas1.bind('<ButtonPress-1>', self.click)

        # Getting center of canvas and setting it
        width = eval(canvas1["width"])
        height = eval(canvas1["height"])
        self.center = (width/2, height/2)

        # Calls method draw_hexagons() to draw in the hexagons
        self.draw_hexagons()
        for hex in self.hexIDs:
            int(self.canvas1.gettags(hex)[0])
        root.mainloop()

HexagonGame(3,"")

