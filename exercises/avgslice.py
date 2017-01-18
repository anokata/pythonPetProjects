xrange = range
def solution(A):
    m = 1000000000
    mi = 0
    n = len(A)
    if n == 2:
        return 0
    for i in xrange(n-2):
        m2 = (A[i] + A[i+1])/2.0
        m3 = (A[i] + A[i+1] + A[i+2])/3.0
        if m2 < m:
            m = m2
            mi = i
        if m3 < m:
            m = m3
            mi = i
    i += 1
    m2 = (A[i] + A[i+1])/2
    if m2 < m:
        m = m2
        mi = i
    return mi

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

a=solution([4,2,2,5,1,5,8])
print(a)

