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

def makeSuccsessiveRooms(n):
    pass

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
