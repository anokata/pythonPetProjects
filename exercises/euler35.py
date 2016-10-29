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


def prime(n):
    e = n
    i = 2
    while i<e:
        if n%i == 0:
            return False
        i+=1
    return True

def roundprime(n):
    x = str(n)
    for i in range(len(x)):
        #print(i, prime(int(x)), x)
        if not primeis(int(x)):
            return False
        x = x[-1] + x[:-1]
    return True

mx = 1000000
genprimes(mx)
print('prime generated')
#print(sorted(list(primed)))
c = 1
for x in range(3, mx):
    if roundprime(x):
        c += 1
print(c)
