from scipy import misc
import numpy as np
from PIL import Image, ImageDraw

# Radius of Hexagon Required
r = 50
# Center Points
cX = 50
cY = 50

# Creates the mask and masks the image
# PARAM (maskBase) - Base image the mask is derived from
def maskImage(maskBase):
    bg = Image.open("images/blueDragon.jpg").copy()
    x, y = bg.size[0]/2, bg.size[1]/2
    image = sliceBackground(bg, x, y)
    if image.mode == "RGB":
        image = np.array(image.getdata()).reshape(image.size[0], image.size[1], 3)
    else:
        image = np.array(image.getdata()).reshape(image.size[0], image.size[1], 4)
    row, col, z = image.shape
    # Getting base image data to create the mask
    mask = np.array(maskBase.getdata()).reshape(maskBase.size[0], maskBase.size[1], 3)

    # Creating the mask
    if z == 3:
        image = np.dstack((image, np.full((row, col), 255)))
        mask = np.dstack((mask, np.full((mask.shape[0], mask.shape[1]), 255)))
    for r in range(0, row):
        for c in range(0, col):
            if np.all(mask[r][c] == [0, 0, 0, 255]):
                mask[r][c] = (0, 0, 0, 0)
            else:
                mask[r][c] = (1, 1, 1, 1)
    print mask

    # Mask the image and save it
    maskedImage = np.ma.masked_array(image, mask=mask)
    maskedImage = maskedImage.filled([0, 0, 0, 0])
    misc.toimage(maskedImage, cmin=0.0, cmax=256.0).save('outfile.png')

# Returns the points on a hexagon centered at 50, 50 for this demo
def hexagonPoints():
    points = []
    for k in range(6):
        x, y = cX + r * np.cos(k * np.pi / 3), cY + r * np.sin(k * np.pi / 3)
        points.extend([x, y])
    return points

# Creates the image to use as the mask.
# This image is never saved as it is passed as a parameter to maskImage
def drawMaskImage():
    image2 = Image.new('RGB', (100, 100), 'white')
    draw = ImageDraw.Draw(image2)
    hexagon = hexagonPoints()
    draw.polygon(hexagon, fill='black')
    maskImage(image2)

def sliceBackground(im, x, y):
    left = x - r
    upper = y - r
    right = x + r
    lower = y + r
    cropBox = (left, upper, right, lower)
    return im.crop(cropBox)

drawMaskImage()

