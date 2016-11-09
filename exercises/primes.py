import math
import pickle

N = 10
primes = [2,3,5,7,11,13,17,19,23]
primed = {2,3,5,7,11,13,17,19,23}
a = pickle.load(open('primes.pkl', 'rb'))
primes = a['s']
primed = a['d']
N = a['n']

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
    global N
    if n <= N:
        print('already generated. loaded')
        return
    np = n // 100
    for x in range(N,n):
        p = primeList(x)
        if p:
            primes.append(x)
            primed.add(x)
        if x % np ==0:
            print(str(x//np)+'%')
    print('prime generated')
    pickle.dump({'s':primes, 'd':primed, 'n':n}, open('primes.pkl', 'wb'))
    N = n

def justPrime(n):
    m = int(math.sqrt(n)) + 2
    for x in range(3, m, 2):
        if n%x == 0:
            return False
    return True


