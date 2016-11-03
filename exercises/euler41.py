import primes
from itertools import permutations
n = 7
l = ''.join([chr(x+49) for x in range(n)])
print(l)
all = permutations(l) # max  = 900 050 021
#primes.genprimes(1000000)
nums = list()
for x in all:
    if x[n-1] not in '2468':
        nums.append(int(''.join(x)))
print(nums[:10], len(nums))
nums = list(filter(primes.justPrime, nums))
print(nums[:10], len(nums))
print(max(nums))
