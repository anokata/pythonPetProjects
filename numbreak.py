# Нахождение разложения числа на сумму n последовательных
x=int(input("enter number:"))

def s(n): return sum(list(range(1,n+1)))

def sumpos(t, m, N):
    out = ""
    sm = 0
    for x in range(t, t+m):
        out += str(x) + "+"
        sm += x
        if sm > N: return 0, 0
    out += "=" + str(sm)
    return (out, sm)

m = 2

while (m*(m+1)/2<=x):
    for t in range(1, x):
        out, sm = sumpos(t, m, x)
        if sm == x:
            print("M:", m)
            print(out)
    m += 1
