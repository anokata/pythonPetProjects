import random
import math
random.seed()

def makeHole(r, x, y):
    return list(filter(lambda a: a != (x, y, Wall), r)) + [(x, y, Floor)]

def makeHWall(x, y, w):
    r = list()
    for i in range(x, x + w + 1):
        r.append((i, y, Wall))
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

Wall = '#'
Floor = '.'
Void = '`'
def makeRoom(x, y, w, h):
    r = list()
    w = w - 1
    h -= 1

    for i in range(x, x + w + 1):
        for j in range(y, y + h + 1):
            if i == x or i == x + w or j == y or j == y + h :
                r.append((i, j, Wall))
            else:
                r.append((i, j, Floor))
    return r

def makeVoidStrLst(w, h):
    return (Void * (w+1) + '\n') * (h+1)

def cdr(tup):
    return tup[1]
def car(tup):
    return tup[0]

def setXY(l, x, y, w, val):
    offset = y * (w+1) + x # Перенос строки, поэтому +1
    l = l[:offset] + val + l[offset+1:]
    return l

def calcWidth(l):
    return max(list(map(car, l))) + 1

def lab2StrLst(l):
    w = max(list(map(car, l)))
    h = max(list(map(cdr, l)))
    r = makeVoidStrLst(w, h)
    for x, y, tile in l:
        r = setXY(r, x, y, w+1, tile)
    return r

def getXY(x, y, lab):
    l = lab2StrLst(lab)
    w = calcWidth(lab)
    x = y * (w + 1) + x
    try:
        tile = l[x]
    except:
        return Void
    return l[x]

def isVoid(x, y, lab):
    return getXY(x, y, lab) == Void

def makeLabirintRand(n):
    fieldW = 90
    fieldH = 25
    minwh = 5
    maxwh = 10
    rooms = list()
    rooms = makeRoom(0,0, maxwh//2, maxwh//2)
    for i in range(n):
        done = False
        while not done:
            w = random.randint(minwh, maxwh)
            h = random.randint(minwh, maxwh)
            x = random.randint(0, fieldW)
            y = random.randint(0, fieldH)
            right = x + w - 1
            bottom = y + h - 1
            done = isVoid(x, y, rooms) and isVoid(right, y, rooms) and\
                    isVoid(x, bottom, rooms) and isVoid(right, bottom, rooms) and\
                    isVoid(x + w // 2, y + h // 2, rooms)
            #rooms.append((x, y, '+'))
            #rooms.append((right, bottom, '*'))
            #rooms.append((right, y, '>'))
            #rooms.append((x, bottom, '<'))
            #print(lab2StrLst(rooms))
            #import time
            #time.sleep(0.5)

        rooms += makeRoom(x, y, w, h)

    return rooms


if __name__ == '__main__':
    r = makeLabirintRand(20)
    print(lab2StrLst(r))



