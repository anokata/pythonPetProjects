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
    a = 0
    while not(a*a <= x and (a+1)**2 >x):
        a += 1
    return a

def stolbik(x):
    res = ''
    xx = str(x)
    if len(xx) % 2 == 1:
        xx = '0'+xx
    x = [x+y for x, y in zip(xx[::2], xx[1::2])]
    print(x)
    z = int(x[0])
    a = finda(z)
    res += str(a)
    nx = int(x[0]) - a*a
    nx = nx*100 + int(x[1])
    print(a, nx)
    b = res * 20

stolbik(69696)
