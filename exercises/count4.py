xrange = range
def solution(A):
    n = len(A)
    A.sort()
    if A[0] > 1:
        return 1
    if n == 1:
        if A[0] <=0 or A[0] > 1:
            return 1
        else:
            return 2
    print(A, A[-1])
    if A[-1] < 0:
        return 1
    for i in xrange(n-1):
        if A[i] < 0 and A[i+1] > 1:
            return 1
        elif A[i] > 0 and A[i+1] - A[i] > 1:
            return A[i] + 1
    return A[-1] + 1
    
assert(            
            
        
    
