xrange = range
def solution(A):
    n = len(A)
    if n == 1:
        return 1
    size = 0
    ssize = 0
    pre_lead = [0] * n
    suf_lead = [0] * n
    for i in xrange(n):
        if size == 0:
            size += 1
            value = A[i]
            pre_lead[i] = value
        else:
            if value != A[i]:
                size -= 1
            else:
                size += 1
                pre_lead[i] = value
        if ssize == 0:
            ssize += 1
            svalue = A[n-1-i]
            suf_lead[i] = svalue
        else:
            if svalue != A[n-1-i]:
                ssize -= 1
            else:
                ssize += 1
                suf_lead[i] = svalue
    print(pre_lead)
    print(suf_lead)
    eql = 0
    for i in xrange(n):
        if pre_lead[i] != 0 and pre_lead[i] == suf_lead[i]:
            eql += 1
    return eql
