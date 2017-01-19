xrange = range

def difsign(a, b):
    return (a > 0 and b < 0) or (a < 0 and b > 0)

def solution(a):
    hv = 0
    if len(a) == 1:
        return 1
    #if a[-1] > 0:
        #a.append(-1)
    #else:
        #a.append(0)
    n = len(a)
    pred = 0
    lastdif = 0
    for i in xrange(0, n):
        if a[i] - pred != 0:
            dif = a[i] - pred
            #print(dif, lastdif, pred, difsign(dif, lastdif))
            pred = a[i]
            #print(i, 'i',n-1, hv == 1 and i == n-1)
            if difsign(dif, lastdif):# and (i != 0 and i!=n-1): #and not (hv == 1 and i == n-1):
                hv += 1
                #print(i)
            lastdif = dif

    print('a', hv)
    if hv != 0:
        if a[0] != a[-1]:
            hv += 2
        else:
            hv += 2
    else:
        hv = 1
    
    print('an', hv)
    return hv

assert(solution([2,2,3,4,3,3,2,2,1,1,2,5]) == 4)
assert(solution([-1,-1]) == 1)
assert(solution([1]) == 1)
assert(solution([1,1]) == 1)
assert(solution([1,1,1,1]) == 1)
assert(solution([1,2,1]) == 3)
assert(solution([1,2,3]) == 1)
assert(solution([1,2,3,2]) == 3)

