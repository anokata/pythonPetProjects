def periodlen(x):
    p = 1
    n = 10000
    x = str(10**n//x).rstrip('0')
    if len(x) < n//10:
        return (0, '')

    while True:
        if x[:p] == x[p:p+p]:
            return (p, x[:p])
        p += 1
        if p >= len(x)-1:
            x = x[1:]
            p = 1
        if len(x) == 1:
            return (-1, '')

def findmax(n):
    m = a = 0
    p = ''
    for x in range(10, n):
        period, per = periodlen(x)
        if period > m:
            m = period
            a = x
            p = per
    return (m, a, p)
print(findmax(1001))
