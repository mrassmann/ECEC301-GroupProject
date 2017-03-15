from scipy import misc
import numpy as np
from PIL import Image, ImageDraw

def maskImage(maskBase):
    image = misc.imread("canvas_rose_red.gif")
    row, col, z = image.shape
    mask = np.array(maskBase.getdata()).reshape(maskBase.size[0], maskBase.size[1], 3)
    if z == 3:
        image = np.dstack((image, np.full((row, col), 255)))
        mask = np.dstack((mask, np.full((row, col), 255)))
    for r in range(0, row):
        for c in range(0, col):
            if np.all(mask[r][c] == [0, 0, 0, 255]):
                mask[r][c] = (0, 0, 0, 0)
            else:
                mask[r][c] = (1, 1, 1, 1)

    print mask
    maskedImage = np.ma.masked_array(image, mask=mask)
    maskedImage = maskedImage.filled([0, 0, 0, 0])
    misc.toimage(maskedImage, cmin=0.0, cmax=256.0).save('outfile.png')


def hexagon_generator():
    """Generator for coordinates in a hexagon."""
    points = []
    for k in range(6):
        x, y = 50 + 50 * np.cos(k * np.pi / 3), 50 + 50 * np.sin(k * np.pi / 3)
        points.extend([x, y])
    return points

def main():
    image2 = Image.new('RGB', (100, 100), 'white')
    draw = ImageDraw.Draw(image2)
    hexagon = hexagon_generator()
    draw.polygon(hexagon, fill='black')
    maskImage(image2)

main()

