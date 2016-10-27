from PIL import Image, ImageDraw
def mandn(p, q, n):
    x = p
    y = q
    for i in range(n):
        x, y = (x**2 - y**2 + p), (2*x*y + q)
        z = x**2 +y**2
        if z > 4:
            break
    return i

w = h = 512
deep = 50
im = Image.new("RGB", (w, h), "white")
draw = ImageDraw.Draw(im)
#pix = im.load()
for x in range(w):
    for y in range(h):
        i = x - w//1.6
        j = y - w//1.6
        i /= 180.0
        j /= 180.0
        s = mandn(i, j, deep)
        s = 255 * s/float(deep)
        s = int(s)
        r = g = s
        #r = s % 85
        #g = s % 170
        draw.point((x,y), (r,g,s))
im.show()
