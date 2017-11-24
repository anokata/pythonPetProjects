import primes
n = 1000000
primes.genprimes(n)
m10 = [0 for x in range(10)]
for p in primes.primes:
    m10[p%10] += 1

for i,a in enumerate(m10):
    print(i,a)

print(m10[1])
print(m10[3])
print(m10[7])
print(m10[9])
print(m10[1]/m10[3])

m10 = [0 for x in range(123)]
for p in primes.primes:
    m10[p%100] += 1

for i,a in enumerate(m10):
    if (a>1):
        print(i,a)
