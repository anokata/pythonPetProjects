xrange = range
def solution(A):
    n = len(A)
    if n == 0:
        return -1
    half = n//2
    size = 0
    idx = 0
    count = 0
    for i in xrange(n):
        if size == 0:
            size += 1
            value = A[i]
            idx = i
        else:
            if value != A[i]:
                size -= 1
            else:
                size += 1
    
    if size > 0:
        for x in A:
            if x == value:
                count += 1
                if count > half:
                    return idx
    return -1
