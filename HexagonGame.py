from Tkinter import *
import numpy as np

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
        for hex in self.hexIDs:
            if int(self.canvas1.gettags(hex)[1]) == 100:
                self.canvas1.delete(hex)

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

        root.mainloop()

# Call the game to begin
HexagonGame(3, "")

