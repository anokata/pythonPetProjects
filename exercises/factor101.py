xrange = range
from math import sqrt
def solution(N):
    import math
    if N in [1, 2, 3]:
        return N
<<<<<<< Updated upstream
    n = int(sqrt(N)) + 1
    c = 2
    for i in xrange(2, n):
=======
    n = int(math.sqrt(N)) + 1
    c = 1
    for i in xrange(1, n):
>>>>>>> Stashed changes
        if not N % i:
            c += 2
    if n * n == N:
        c += 1
    return c
print(solution(17))
assert(solution(24) == 8)
assert(solution(17) == 2)
