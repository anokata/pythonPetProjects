import primes

N = 1000000
start = 0
length = 2
f = list()
primes.genprimes(N)
L = len(primes.primes)
maxl = 0
maxn = 0
i = 0

for start in range(0, L//20):
    for length in range(20000, 200100):
        i += 1
        if i % 10000 == 0:
            print(start, length)
        ll = primes.primes[start:start+length]
        n = sum(ll)
        if n < N and n in primes.primed:
            if length > 540:
                pass
                #print('>', n, ll)
            if maxl < length:
                print(maxl, n)
                maxl = length
                maxn = (n, ll)

print(maxl, maxn)
