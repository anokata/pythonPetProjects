a=[0]*10
b=[0]*16
for x in range(1, 10):
    c = int(str(2**x)[0])
    h = int(str(2**x)[0], 3)
    print(h)
    #print(c)
    a[c] += 1
    b[h] += 1
print(list(range(10)))
print(a)
print(b)
