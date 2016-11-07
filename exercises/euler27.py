import primes
primes.genprimes(100000)

def maxprime(a, b):
    n = 0
    r = 2
    while r in primes.primed:
        r = n*n + n*a + b
        n += 1
    return n-1

print(maxprime(-79, 1601))
ma = mb = d = 0
r = 0
l = list()

for a in range(-1000, 1001):
    for b in range(2, 1001):
        if b in primes.primed:
            m = maxprime(a, b)
            if m > r:
                r = m
                ma = a
                mb = b
                d = a*b
                l.append((a,b))
print(ma, mb, d, r)

