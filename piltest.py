import random
from PIL import Image, ImageDraw

img = 'ts.jpg'
image = Image.open(img)
draw = ImageDraw.Draw(image)
w = image.size[0]
h = image.size[1]
pix = image.load()
dep = 20

for i in range(w):
  for j in range(h):
    r = pix[i, j][0]
    g = pix[i, j][1]
    b = pix[i, j][2]
    s = (r + g + b) // 3
    r = s + dep * 2
    g = s + dep
    b = s
    if r > 255:
      r = 255
    if g > 255:
      g = 255
    if b > 255:
      b = 255
    draw.point((i, j), (r,g,b))

image.save("out"+img, "JPEG")
del draw
