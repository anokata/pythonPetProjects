xrange = range
def solution(A):
    left_sum = 0
    right_sum = 0
    n = len(A)
    print(n, A)
    for p in xrange(n):
        left_sum = sum(A[:p])
        right_sum = sum(A[p+1:])
        print(left_sum, right_sum, p, A[:p], A[p+1:])
        if left_sum == right_sum:
            return p
    
    return -1

print (solution( [-1, 3, -4, 5, 1, -6, 2, 1]))
