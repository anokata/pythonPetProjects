n = 3000000
def genT(x):
    s = set()
    for n in range(1,x):
        s |= {n*(n+1)//2}
    return s
t = genT(n)
def genP(x):
    s = set()
    for n in range(1,x):
        s |= {n*(3*n-1)//2}
    return s
p = genP(n)
def genH(x):
    s = set()
    for n in range(1,x):
        s |= {n*(2*n-1)}
    return s
h = genH(n)
a = t & p & h
#print(a, 40755 in t, 40755 in p)
print(a)
