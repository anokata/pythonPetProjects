import primes
n = 1000000
compounds = set(range(100000,n)) - primes.primed
primes.genprimes(n)

def factors(x):
    factors = 0
    n_prime = 0
    p = primes.primes[n_prime]
    is_same = False
    while x >= p:
        if x % p == 0:
            x = x // p
            if not is_same:
                factors += 1
                is_same = True
        else:
            n_prime += 1
            p = primes.primes[n_prime]
            is_same = False
    return factors

inline = list()
line = list()
z = n//100
for x in compounds:
    f = factors(x)
    if x % z==0:
        print('...')
    if f == 4:
        line.append(x)
    else:
        if len(line)>3:
            print(x)
            inline.append(line)
            break
        line = list()

print(line, inline[:3])
