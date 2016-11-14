import random

WALL = 0
FLOOR = 1
PLAYER = 8
TELEPORT = 3
INIT = 4

DrawChars = {
        WALL: 'x',
        FLOOR: '.',
        PLAYER: '~',
        TELEPORT: 'T',
        INIT: 'o',
        }

def addRectBorder(m, w, val=WALL):
    for x in (0, w-1):
        for y in range(len(m)):
            m[x][y] = val
    for y in (0, w-1):
        for x in range(len(m)):
            m[x][y] = val

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

def stepn(m):
    BL = 4
    DL = 3
    n = init_matrix(len(m))
    for x in range(1, len(m) - 2):
        for y in range(1, len(m) - 2):
            ne = calcNei(m, x, y)
            c = m[x][y]
            if c == WALL:
                if ne > BL:
                    n[x][y] = FLOOR
            else:
                if ne >= DL:
                    n[x][y] = FLOOR
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
    m = [[WALL for x in range(w)] for y in range(w)]
    return m

def objects_generate(m, TL=4):
    for x in range(1, len(m)-1):
        for y in range(1, len(m)-1):
            ne = calcNei(m, x, y)
            if ne < TL and m[x][y] == FLOOR:
                m[x][y] = 3

def randomize(m, chance=55):
    for x in range(0, len(m)):
        for y in range(0, len(m)):
            c = random.randint(0,100)
            if c > chance:
                m[x][y] = FLOOR
    return m

def gen(w=100, steps=3):
    m = init_matrix(w)
    m = randomize(m)
    for i in range(steps):
        m = stepn(m)
    objects_generate(m)
    #floodFill(m, 20, 20, m[20][20], 2)
    addRectBorder(m, w)
    placePlayer(m)
    return m

def getRandomFreePoint(m):
    x = 0
    y = 0
    w = len(m)
    notFree = True
    while notFree:
        x = random.randint(2, w-2)
        y = random.randint(2, w-2)
        n = calcNei(m, x, y)
        notFree = n < 7
        #notFree = m[x][y] == FLOOR
    return (x, y)

def placePlayer(m):
    x, y = getRandomFreePoint(m)
    m[x][y] = PLAYER
    return m

def drawString(m):
    r = str()
    for x in range(0, len(m)):
        for y in range(0, len(m)):
            char = DrawChars[m[x][y]]
            r += char
        r += '\n'
    return r

m = gen(30, 5)
if __name__ == '__main__':
    print(drawString(m))


