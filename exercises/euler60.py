import primes
n = 10
primeindex = 0
N = 5

def prime_index_to_primes(i):
    ps = list()
    pi = primes.primes[i]
    for i in range(N):
        ps.append(pi)
        pi, p = divmod(pi, n)
        pi = primes.primes[p]
    return ps

for i in range(10,20):
    print(prime_index_to_primes(i))
    
