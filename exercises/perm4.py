xrange = range
def solution(A):
    A.sort()
    n = len(A)
    if A[0] != 1 or A[-1] != n:
        return 0
    for i in xrange(1, n-1):
        if A[i] != i+1:
            return 0
    return 1

assert(solution([1]) == 1)
assert(solution([1,2]) == 1)
assert(solution([1,2,3]) == 1)
assert(solution([3,2,1]) == 1)
assert(solution([3,2,2]) == 0)
assert(solution([1,2,2]) == 0)
assert(solution([1,2,1]) == 0)
assert(solution([1,1,1]) == 0)
assert(solution([1,1]) == 0)
assert(solution([2,3]) == 0)
assert(solution([2,3]) == 0)
