import random
import math
random.seed()

def makeHole(r, x, y):
    return list(filter(lambda a: a != (x, y), r))

def makeHWall(x, y, w):
    r = list()
    for i in range(x, x + w + 1):
        r.append((i, y))
    return r

def makeTunnelH(r, sx, y, ex):
    r = makeHole(r, sx, y)
    r = makeHole(r, ex, y)
    r += (makeHWall(sx, y+1, ex-sx))
    r += (makeHWall(sx, y-1, ex-sx))
    return r


def makeRoomWithHoles(x, y, w, h):
    r = makeRoom(x, y, w, h)
    l = (w + h) // 4
    if w > l:
        #r = list(filter(lambda a: a != (l+x, y) and a != (l+x, y+h), r))
        r = makeHole(r, l+x, y)
        r = makeHole(r, l+x, y+h)

    if h > l:
        r = list(filter(lambda a: a != (x, y+l) and a != (x+w, y+l), r))

    return r

def makeRoom(x, y, w, h):
    r = [(x, y)]
    for i in range(x + 1, x + w + 1):
        r.append((i, y))

    for i in range(x + 1, x + w + 1):
        r.append((i, y + h))

    for i in range(y + 1, y + h + 1):
        r.append((x, i))

    for i in range(y + 1, y + h + 1):
        r.append((x + w, i))
    return r

def makeVoidStrLst(w, h):
    return ('.' * (w+1) + '\n') * (h+1)

def cdr(tup):
    return tup[1]
def car(tup):
    return tup[0]

def setXY(l, x, y, w, val):
    offset = y * (w+1) + x # Перенос строки, поэтому +1
    l = l[:offset] + val + l[offset+1:]
    return l

def lab2StrLst(l):
    w = max(list(map(car, l)))
    h = max(list(map(cdr, l)))
    r = makeVoidStrLst(w, h)
    for x, y in l:
        r = setXY(r, x, y, w+1, '#')
    return r

def makeRecLab():
    fieldW = 90
    fieldH = 25
    minwh = 5
    maxwh = 10
    dens = 3
    roomcount = 10
    rs = list()

    x = fieldW // 2
    y = fieldH // 2

    def r(x, y, rooms, count):
        if count == 0:
            return
        w = random.randint(minwh, maxwh)
        h = random.randint(minwh, maxwh)
        rooms += makeRoom(x, y, w, h)

        exits = random.randint(1, 4)
        for i in range(exits):
            updownleftright = random.randint(1, 4)
            if updownleftright == 1: # up
                y -= h//2 + dens + maxwh//2
            if updownleftright == 2: # down
                y += h//2 + dens + maxwh//2
            if updownleftright == 3: # left
                x -= w//2 + dens + maxwh//2
            if updownleftright == 4: # right
                x += w//2 + dens + maxwh//2
            room = r(x, y, rooms, count - 1)
            if room:
                rooms += room
        return rooms

    rs = r(x, y, rs, roomcount)

    return rs


def makeLabirint():
    # сделаем комнаты по другому- комната это точка центра и ширина и высота.
    roomcount = 8
    fieldW = 90
    fieldH = 25
    minwh = 5
    centers = list()
    rooms = list()
    rms = list()
    labirint = list()
    # Сгенерируем на площади рандомно множество точек - центров
    for i in range(roomcount):
        x = random.randint(0, fieldW)
        y = random.randint(0, fieldH)
        centers.append((x, y))
    # вычислим ширину и высоту комнат от этих центров так чтобы они не пересекались
    # натий от каждой точки ближайшие, дистанцию
    for x,y in centers:
        distances = [math.sqrt((x-a)*(x-a)+(y-b)*(y-b)) for a,b in centers]
        distances.sort()
        minDistance = (math.floor(distances[1]))
        if minDistance < minwh + 1:
            continue
        rooms.append((x, y, minDistance))

    for x,y,d in rooms:
        w = random.randint(minwh, d-1)
        h = random.randint(minwh, d-1)
        labirint.append((x, y, w, h))
        rms += makeRoom(x, y, w, h)
        
    return rms


def makeSuccsessiveRooms(n):
    minwh = 2
    maxwh = 10
    lastX = 0
    lastY = 0
    density = 8
    rooms = list()
    for i in range(n):
        w = random.randint(minwh, maxwh)
        h = random.randint(minwh, maxwh)
        x = lastX + random.randint(1, density)
        y = lastY + random.randint(1, density)
        room = makeRoom(x, y, w, h)
        lastX = x + w
        lastY = y + h
        rooms += room
    return rooms

if __name__ == '__main__':
    # test
    r = makeRoom(2,8, 4, 4)
    r += makeRoom(0,0, 3, 6)
    r += makeRoomWithHoles(9,1, 5, 5)
    r += makeRoomWithHoles(9,8, 5, 5)
    r += makeRoom(9,15, 5, 5)
    print(r)
    r = makeTunnelH(r, 6, 10, 9)
    print(r)
    print(lab2StrLst(r))
    print(setXY('aaaaaaaaa', 1, 1, 3, 'z'))
    r = (makeSuccsessiveRooms(3))
    print(lab2StrLst(r))
    r = makeLabirint()
    print(lab2StrLst(r))
    r = makeRecLab()
    print(lab2StrLst(r))

