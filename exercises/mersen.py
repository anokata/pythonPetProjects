import primes

#p = primes.primes[i]

def mersen(p):
    return 2**(p) - 1

def is_prime_mersen(n):
    if primes.justPrime(n):
        print("{} is prime".format(n))
    else:
        print("{} not is prime".format(n))

def test_mersen_to(n):
    for i in range(1, n):
        p = mersen(primes.primes[i])
        print("test {} ".format(p), end='\t---\t ')
        if primes.justPrime(p):
            print("M#{} = 2^{} -1 = {} is prime".format(i, primes.primes[i], p))
        else:
            print("   2^{} -1 = {} is not prime".format(i, primes.primes[i], p))

if __name__ == "__main__":
    test_mersen_to(18)
