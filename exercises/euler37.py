import primes
n = 1000000
primes.genprimes(n)
def shortedprime(x):
    if not primes.primeis(x):
        return False
    rstr = str(x)
    lstr = str(x)
    leftRight = False
    while len(rstr) > 1:
        if leftRight:
            rstr = rstr[1:]
            lstr = lstr[:-1]
        else:
            lstr = lstr[1:]
            rstr = rstr[:-1]
        #print(rstr, lstr, 'a')
        if not primes.primeis(int(rstr)) or not primes.primeis(int(lstr)):
            return False
    return True
sm = 0
for i in range(10,n):
    if shortedprime(i):
        print(i)
        sm +=i


print(sm)


