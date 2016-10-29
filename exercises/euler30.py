
def isSum4(n):
    x = n
    n = str(n)
    a, b, c, d = int(n[0]), int(n[1]), int(n[2]), int(n[3])
    sm = a**4 + b**4 +c**4 + d**4
    return sm == x

def dum4():
    n = 1000
    s = 0
    for x in range(n, 10000):
        if isSumn(x,4):
            s += x
            print("x: {}, sum:{}".format(x, s))

def isSum5(n):
    x = n
    n = str(n)
    a, b, c, d, e = int(n[0]), int(n[1]), int(n[2]), int(n[3]), int(n[4])
    sm = a**5 + b**5 +c**5 + d**5 + e**5
    return sm == x

def isSumn(n, p):
    x = n
    n = str(n)
    sm = 0
    for i in n:
        sm += int(i) ** p
    return sm == x

def dum5():
    s = 0
    for x in range(100, 1000000):
        if isSumn(x,5):
            s += x
            print("x: {}, sum:{}".format(x, s))
#dum4()
dum5()
