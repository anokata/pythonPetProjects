xrange = range
from math import sqrt
def solution(N):
    if N in [1, 2, 3]:
        return N
    n = int(sqrt(N)) + 1
    c = 2
    for i in xrange(2, n):
        if not N % i:
            c += 2
    if n * n == N:
        c += 1
    return c
print(solution(17))
assert(solution(24) == 8)
assert(solution(17) == 2)
