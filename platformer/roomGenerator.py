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

if __name__ == '__main__':
    # test
    r = makeRoom(2,8, 4, 4)
    print(r)
    r += makeRoom(0,0, 3, 6)
    r += makeRoom(9,1, 5, 5)
    r += makeRoom(9,8, 5, 5)
    r += makeRoom(9,15, 5, 5)
    print(lab2StrLst(r))
    print(setXY('aaaaaaaaa', 1, 1, 3, 'z'))
