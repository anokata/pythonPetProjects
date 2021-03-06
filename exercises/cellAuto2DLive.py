from PIL import Image, ImageDraw
import random
w = 200
img = Image.new("RGB", (w*3, w*3), 'black')
draw = ImageDraw.Draw(img)


def drawm(m, h=3):
    for x in range(0, len(m)):
        for y in range(0, len(m)):
            if m[x][y] == 1:
                #draw.point((x,y), (0,0,255))
                draw.rectangle([x*h, y*h, x*h+h, y*h+h], (0, 0, 200))
            elif m[x][y] == 2:
                draw.rectangle([x*h, y*h, x*h+h, y*h+h], (200, 0, 0))
            elif m[x][y] == 3:
                draw.rectangle([x*h, y*h, x*h+h, y*h+h], (200, 200, 0))
            else:
                draw.rectangle([x*h, y*h, x*h+h, y*h+h], (50, 50, 50))

def floodFill(m, x, y, val, newval):
    tofill = list()
    tofill.append((x, y))
    while len(tofill) != 0:
        x, y = tofill[0]
        tofill.remove((x, y))
        if m[x][y] == val:
            m[x][y] = newval
            tofill.append((x+1, y))
            tofill.append((x-1, y))
            tofill.append((x, y+1))
            tofill.append((x, y-1))
    return m

def play_life():
    for i in range(10):
        m = step(m)
        drawm(m)

def step_life(m):
    n = [[0 for x in range(w)] for y in range(w)]
    for x in range(1, len(m) - 2):
        for y in range(1, len(m) - 2):
            ne = calcNei(m, x, y)
            c = m[x][y]
            if ne == 3 and c == 0:
                n[x][y] = 1
            if c == 1 and (ne == 2 or ne == 3):
                n[x][y] = 1
    return n



def stepn(m):
    BL = 4
    DL = 3
    n = [[0 for x in range(len(m))] for y in range(len(m))]
    for x in range(1, len(m) - 2):
        for y in range(1, len(m) - 2):
            ne = calcNei(m, x, y)
            c = m[x][y]
            if c == 0:
                if ne > BL:
                    n[x][y] = 1
            else:
                if ne >= DL:
                    n[x][y] = 1
    return n

def calcNei(m, x, y):
    r = 0
    r += m[x-1][y]
    r += m[x-1][y-1]
    r += m[x-1][y+1]
    r += m[x+1][y]
    r += m[x+1][y+1]
    r += m[x+1][y-1]
    r += m[x][y-1]
    r += m[x][y+1]
    return r

def init_matrix(w):
    m = [[0 for x in range(w)] for y in range(w)]
    return m

def objects_generate(m, TL=4):
    for x in range(1, len(m)-1):
        for y in range(1, len(m)-1):
            ne = calcNei(m, x, y)
            if ne < TL and m[x][y] == 1:
                m[x][y] = 3

def randomize(m, chance=55):
    for x in range(0, len(m)):
        for y in range(0, len(m)):
            c = random.randint(0,100)
            if c > chance:
                m[x][y] = 1
    return m

def gen(w=100, steps=3):
    m = init_matrix(w)
    m = randomize(m)
    for i in range(steps):
        m = stepn(m)
    objects_generate(m)
    #floodFill(m, 20, 20, m[20][20], 2)
    return m

def drawString(m):
    r = str()
    for x in range(0, len(m)):
        for y in range(0, len(m)):
            if m[x][y] == 1:
                r += '.'
            elif m[x][y] == 2:
                r += '#'
            elif m[x][y] == 3:
                r += 'T'
            else:
                r += 'x'
        r += '\n'
    return r

m = gen(30, 5)
#drawm(m, 12)
print(drawString(m))
#img.show()





