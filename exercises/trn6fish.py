
def solution(A, B):
    n = len(A)
    N = n
    last = 0
    for i in xrange(N):
        #print i, last, n
        if B[i] == 1:
            last = A[i]
        elif i != 0 and last > A[i]:
            n -= 1
        elif i != 0:
            n -= 1
            last = A[i]      
        #print i, last, n
    return n
