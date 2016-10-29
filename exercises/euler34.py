import math
def facnum(n):
    x = str(n)
    s = 0
    for i in x:
        f = math.factorial(int(i))
        s += f
        #print(i,f)
    return s
#print(facnum(145))

sm = 0
for x in range(3,10000000):
    if facnum(x) == x:
        sm += x
        print(x, sm)
