from scipy import misc
import numpy as np
import math
from PIL import Image, ImageDraw

image = misc.imread('problem3.jpg')
row, col, z = image.shape
if z == 3:
    mask = np.zeros((row, col, 4))
    flag = False
    for r in range(0, row+1):
        if r % 50 == 0:
            flag = not flag
        if flag:
            mask[r:] = (1, 1, 1, 1)
        else:
            mask[r:] = (0, 0, 0, 0)
    image = np.dstack((image, np.full((row, col), 255)))

maskedImage = np.ma.masked_array(image, mask=mask)
maskedImage = maskedImage.filled([0, 0, 0, 0])
print maskedImage
misc.toimage(maskedImage, cmin=0.0, cmax=256.0).save('outfile.png')


def hexagon_generator(edge_length, offset):
    """Generator for coordinates in a hexagon."""
    x, y = offset
    for angle in range(0, 360, 60):
        x += math.cos(math.radians(angle)) * edge_length
        y += math.sin(math.radians(angle)) * edge_length
        yield x, y

def main():
    image2 = Image.new('RGB', (100, 100), 'white')
    draw = ImageDraw.Draw(image2)
    hexagon = hexagon_generator(50, offset=(20, 0))
    draw.polygon(list(hexagon), fill='red')
    image2.show()

main()

