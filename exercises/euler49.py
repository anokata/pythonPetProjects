import primes
from itertools import permutations
primes.genprimes(1000)
p = set(primes.primed)
primes.genprimes(10000)
p = primes.primed - p

def pemutes(x,y,z):
    a = str(x)
    perms = permutations(a)
    yy = zz = False
    for pr in perms:
        a = int(''.join(pr))
        if y==a:
            yy = True
        if z==a:
            zz = True
        if zz and yy:
            return True
    return False

print(pemutes(4093,5437,6781))
print(4093 in p, 5437 in p, 6781 in p)
i = 0
for p1 in p:
    for p2 in p:
        if p2>p1:
            for p3 in p:
                if p3>p2:
                    if p1!=p2!=p3:
                        d1 = p1-p2
                        d2 = p2-p3
                        if d1==d2 and abs(d1) == 3330:
                            i += 1
                            if i%300==0:
                                print(p1,p2,p3,d1,d2)
                            if pemutes(p1,p2,p3):
                                print('found', p1,p2,p3,d1,d2)
                                exit()
