def pal(n):
    x = int(''.join(reversed(str(n))))
    bn = bin(x)[2:]
    b = int(''.join(reversed(bn)))
    return x == n and b == int(bn)
sm = 0
for x in range(1,1000000):
    if pal(x):
        #print(x)
        sm += x
print(sm)
