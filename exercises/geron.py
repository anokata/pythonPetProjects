def geron(x, e=10):
    xi = 1
    xl = 2
    e = 0.1 ** e
    while abs(xl-xi) > e:
        xl = xi
        xi = 0.5 * ( xi + x/xi)
    return xi

print(geron(25))

def finda(x):
    print('finda', x)
    a = 0
    while not(a*a <= x and (a+1)**2 >x):
        a += 1
    return a

def findap(x, b):
    print('findap', x,b)
    a = 0
    while not((b+a)*a <= x and (b + a + 1)*(a+1) > x):
        a += 1
    return a

def stolbik(x):
    res = ''
    nx = 0
    i = 0
    xx = str(x)
    if len(xx) % 2 == 1:
        xx = '0'+xx
    x = [x+y for x, y in zip(xx[::2], xx[1::2])]
    x += (['00']*100)
    while nx !=0 or i==0:
        c = nx*100 + int(x[i])
        a = finda(c)
        res += str(a)
        nx = int(x[i]) - a*a
        #c = nx*100 + int(x[i+1])
        b = int(res) * 20
        d = findap(c, b)
        res += str(d)
        nx = c - (b + d)*d
        i += 2
        print(nx, i, res)
    print(res, int(res)**2)

stolbik(69696)
