xrange = range
def solution(A):
    pre = list()
    suf = list()
    pre.append(A[0])
    suf.append(A[-1])
    minavg = 0
    minavgind = 0
    n = len(A)
    for i in xrange(1, n):
        pre.append(pre[i-1] + A[i])
        suf.append(suf[i-1] + A[n-i-1])

    print(A, pre, suf)
    return minavgind
        
solution([4,2,2,5,1,5,8])

