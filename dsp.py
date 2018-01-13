import math

x = [1,1,1,1,0,0,0,0] # Xk
x = [2,-2,2,-2,2,-2,2,-2] # Xk
N = len(x)

phi = 2*math.pi/N

a = []
b = []

def sum_furie_a(phi, n, x):
    s = 0
    for k in range(n):
        e = x[k] * math.cos(phi * k)
        #print("-> ", k, round(e, 1), x[k], phi * k, math.cos(phi * k))
        s += e
    return s

def sum_furie_b(phi, n, x):
    s = 0
    for k in range(n):
        s += -1 * x[k] * math.sin(phi * k)
    return s

for n in range(N):
    a.append(0)
    b.append(0)
    a[n] = round(sum_furie_a(phi * n, N, x), 2)
    b[n] = round(sum_furie_b(phi * n, N, x), 2)
    print("n={} \t a={} \t b={}".format(n, a[n], b[n]), end=" ")
    print()


#print(n)
print(a)
print(b)
#print(sum_furie(math.sin, 1, math.pi/4, N, x))
#print(phi, math.pi/4)
