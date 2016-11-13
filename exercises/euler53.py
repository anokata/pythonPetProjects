from math import factorial
def C(n, r):
    return factorial(n)//(factorial(r)*factorial(n-r))

count = int()
for n in range(1, 101):
    for r in range(1, n+1):
        c = C(n, r)
        if c >= 1000000:
            count += 1
print(count)
