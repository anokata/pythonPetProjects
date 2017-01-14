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
        
