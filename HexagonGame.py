from Tkinter import *
import numpy as np
from scipy import misc
from PIL import Image, ImageDraw

class HexagonGame(object):
    def __init__(self, num_rings, img_path):
        self.numRings = num_rings
        self.imgPath = img_path
        self.rings = []
        # Draw more hexagons
        self.hexIDs = []  # A list of IDs for all your hexagons
        self.canvas1 = None
        self.r = 50
        self.center = ()
        self.baseMask = self.drawMaskImage()
        self.run_game()

    def center_point(self, m, n):
        xc = self.center[0]
        yc = self.center[1]
        cc = np.array([xc, yc])  # Center of the canvas.

        # the magic translation vectors for a hexagonal tesselation.
        # With numpy, vectors (and matrices for that matter) are just Python arrays
        v1 = self.r * np.array([1 + np.cos(np.pi / 3), np.sin(np.pi / 3)])
        v2 = self.r * np.array([1 + np.cos(np.pi / 3), -np.sin(np.pi / 3)])  # Only a sign difference.
        z = m * v1 + n * v2 + cc  # Be sure to add the canvas center.
        return z

    def draw_hexagons(self):
        for m in range(-4, 5):
            for n in range(-4, 5):
                color = "cyan"
                outline = "black"
                z = self.center_point(m, n)
                cc = np.array(self.center)
                ring_radius = np.linalg.norm(z - cc) / self.r
                print ring_radius
                ring_radius = round(ring_radius, 3)
                if 0 < ring_radius < 2:
                    ring_number = 1
                    color = "magenta"
                elif 2 < ring_radius < 4:
                    ring_number = 2
                    color = "purple"
                elif self.numRings == 3:
                    if 4 < ring_radius < 6:
                        ring_number = 3
                        color = "cyan"
                else:
                    ring_number = 100
                    color = ""
                if ring_radius == 0.0:
                    ring_number = 100
                self.rings.append(ring_radius)
                points = []
                if ring_radius < 6:
                    for k in range(6):
                        x, y = z[0] + self.r * np.cos(k * np.pi / 3), z[1] + self.r * np.sin(k * np.pi / 3)
                        points.extend([x, y])  # Use extend to add more than one item to a list at a time.
                    newHexID = self.canvas1.create_polygon(points, fill=color, activefill="beige", outline=outline, width=1)
                    self.hexIDs.append(newHexID)
                    self.canvas1.itemconfig(newHexID, tags=(str(ring_number)))

        removedList = []
        for hex in self.hexIDs:
            if int(self.canvas1.gettags(hex)[0]) == 100:
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

    def run_game(self):
        root = Tk()
        Tk.title = "Making Board Game"

        canvas1 = Canvas(root, width=1000, height=1000, bg="white", highlightthickness=0, bd=0)
        self.canvas1 = canvas1
        canvas1.grid(row=0, column=0)
        Label(root, text="Move mouse over Hexagons").grid()

        width = eval(canvas1["width"])
        height = eval(canvas1["height"])
        self.center = (width/2, height/2)

        self.draw_hexagons()
        for hex in self.hexIDs:
            int(self.canvas1.gettags(hex)[0])
        root.mainloop()

HexagonGame(3,"")

