from itertools import product
#print(list(product(list('abc'), [1,2])))

def pentaNumberGen(n):
    for x in range(1,n):
        yield (x*(3*x-1)//2)

def generatePentaNumbers(n):
    return list(pentaNumberGen(n))

p = generatePentaNumbers(10000)
ps = set(p)
dd = list()
d = 100
i = 0
for p1, p2 in product(p, p):
    if p1 != p2:
        i += 1
        if i%1000000==0:
            print('.')
        if abs(p1 - p2) in ps:
            #print(p1, p2)
            if (p1 + p2) in ps:
                print(p1, p2)
                dd.append((p1, p2))
                if d > abs(p1 - p2):
                    d = abs(p1 - p2)

print(dd, d)
