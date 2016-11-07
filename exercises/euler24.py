from itertools import permutations

p =list(permutations('0123456789'))
print(''.join(p[1000000-1]))
