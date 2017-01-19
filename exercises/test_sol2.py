xrange = range

def solution(n):
    d = [0] * 30
    l = 0
    while (n > 0):
        d[l] = n % 2
        n //= 2
        l += 1
    #print(d, l, n)
    for p in xrange(1, l//2 + 1):
        ok = True
        for i in xrange(l - p):
            if d[i] != d[i + p]:
                ok = False
                break
        if ok:
            return p
    return -1
assert(solution(955) == 4)
for x in range(1,50):
    print(x, bin(x)[2:],solution(x))

