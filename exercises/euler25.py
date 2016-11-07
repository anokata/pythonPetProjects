fibs = dict()
def fib(n):
    if n < 3:
        return 1
    if n in fibs:
        return fibs[n]
    if n-1 in fibs:
        f1 = fibs[n-1]
    else:
        f1 = fib(n-1)
        fibs[n-1] = f1

    if n-2 in fibs:
        f2 = fibs[n-2]
    else:
        f2 = fib(n-2)
        fibs[n-2] = f2

    fibs[n] = f1 + f2

    return f1 + f2

m = 0
n = 100
while m < 1000:
    f = fib(n)
    m = len(str(f))
    n += 1
print(n-1, f, len(str(f)))
print(list(fibs.values())[:10])
print(list(fibs.values())[4780:4785])
