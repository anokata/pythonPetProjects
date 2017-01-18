
def solution(N):
    if N in [1, 2, 3]:
        return N
    n = N // 2 + 1
    c = 1
    for i in xrange(1, n):
        if not N % i:
            c +=1
    return c
    
