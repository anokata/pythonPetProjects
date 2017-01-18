def solution(N, A):
    r = [0] * N
    max = 0
    smax = 0
    for x in A:
        if x <= N:
            if smax != 0:
                if r[x-1] >= smax + 1:
                    r[x-1] += 1
                else:
                    r[x-1] = smax + 1
            else:
                r[x-1] += 1
            if r[x-1] > max:
                max = r[x-1]
        else:
            smax = max
        #print r, x  
    r = map(lambda x: smax if x < smax else x, r)
    return r
