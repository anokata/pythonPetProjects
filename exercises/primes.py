import math
primes = [2,3,5,7,11,13,17,19,23]
primed = {2,3,5,7,11,13,17,19,23}
def primeList(n):
    m = int(math.sqrt(n)) + 2
    for p in primes:
        if p>=m:
            return True
        if n%p == 0:
            return False
    return True

def primeopt(n):
    m = int(math.sqrt(n)) + 2
    for p in primed:
        if p>=m:
            continue
        if n%p == 0:
            return False
    return True

def primeis(n):
    return n in primed

def genprimes(n):
    for x in range(23,n):
        p = primeList(x)
        if p:
            primes.append(x)
            primed.add(x)
        if x % 100000==0:
            print(x)
    print('prime generated')

def justPrime(n):
    m = int(math.sqrt(n)) + 2
    for x in range(3, m, 2):
        if n%x == 0:
            return False
    return True


