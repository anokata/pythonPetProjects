import primes
import time
n = 10000
primes.genprimes(n)
allnums = set(range(n))
allodd = set(range(3,n,2))
notall = set()
for x in allnums:
    for p in primes.primed:
        a = p + 2*x*x
        #print(a)
        #time.sleep(.3)
        notall |= {a}
print((allodd - notall) - primes.primed)
#print(notall)
#print(primes.primed)
