def solution(A):
    n = len(A) - 1
    prefix_sums = [0] * n
    postfix_sums = [0] * n
    prefix_sums[0] = A[0]
    postfix_sums[n-1] = A[n]
    for i in xrange(1, n):
        prefix_sums[i] = prefix_sums[i-1] + A[i]
        postfix_sums[n-i-1] = postfix_sums[n-i] + A[n-i]
    #print prefix_sums, postfix_sums
    min = 100000
    for i in xrange(0, n):
        diff = abs(prefix_sums[i] - postfix_sums[i])
        #print(diff, prefix_sums[i], postfix_sums[i])
        if diff < min:
            min = diff
    return min
        
    
def solution(A):
    a = sorted(A, key=abs)
    m = a[-1] * a[-2] * a[-3]
    if m >= 0:
        return m
    i = -3
    while a[i] < 0:
        i -= 1
    if a[-1] * a[-2] > 0:
        m = a[-1] * a[-2] * a[i]
    elif a[-1] < 0:
        m = a[-3] * a[-2] * a[i]
    else:
        m = a[-1] * a[-3] * a[i]
    return m
