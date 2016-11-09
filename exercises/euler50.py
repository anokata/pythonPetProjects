import primes

N = 1000000
start = 0
length = 2
f = list()
primes.genprimes(N)
L = len(primes.primes)
maxl = 0
maxn = 0

for start in range(0, L//2):
    for length in range(530, 655):
        ll = primes.primes[start:start+length]
        n = sum(ll)
        if n < N and n in primes.primed:
            #print('>', n, ll)
            if maxl < length:
                maxl = length
                maxn = (n, ll)

print(maxl, maxn)
