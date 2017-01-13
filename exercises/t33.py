def solution(A, K):
    if len(A) < 2:
        return A
    if K == 0 or K == len(A):
        return A
    if K > len(A):
        K = K % len(A) 
    p = len(A) - K
    for i in range(K):
        A.insert(0, A[-1])
        A.pop()
    return A
    #return A[p:] + A[:-p-1]

print(solution([1,2,3], 1))
print(solution([3, 8, 9, 7, 6], 3))
