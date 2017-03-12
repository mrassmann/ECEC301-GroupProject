from Tkinter import *
import numpy as np

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
        self.run_game()

    def center_point(self,m, n):
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
                    ring_number = 1;
                    color = "magenta"
                elif 2 < ring_radius < 4:
                    ring_number = 2;
                    color = "purple"
                elif self.numRings == 3:
                    if 4 < ring_radius < 6:
                        ring_number = 3;
                        color = "cyan"
                else:
                    ring_number = 100;
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



        for hex in self.hexIDs:
            if int(self.canvas1.gettags(hex)[0]) == 100:
                self.canvas1.delete(hex)

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
        root.mainloop()

HexagonGame(2,"")

