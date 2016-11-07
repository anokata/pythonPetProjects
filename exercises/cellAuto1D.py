from PIL import Image, ImageDraw

w = h = 512
img = Image.new("RGB", (w, h), 'white')
draw = ImageDraw.Draw(img)

draw.point((1,1), (0,0,0))


cells = ['0'] * w
cells[w//2] = '1'
cells[w//2-5] = '1'
cells[w//2+5] = '1'


def step(cells):
    rules = {
        '000': '1',
        '001': '0',
        '010': '0',
        '011': '0',
        '100': '0',
        '101': '1',
        '110': '0',
        '111': '1',
            }
    newcells = cells[:]
    for i in range(1, len(cells)-2):
        state = cells[i-1] + cells[i] + cells[i+1]
        newvalue = rules[state]
        newcells[i] = newvalue
    return newcells


def drawcells(cells, y):
    for i in range(len(cells)):
        c = cells[i]
        if c == '0':
            draw.point((i,y), (0,0,0))
        else:
            draw.point((i,y), (0,0,255))

for i in range(h):
    drawcells(cells, i)
    cells = step(cells)


img.show()
