import primes

def memory(fun):
    mem = dict()
    def wraper(*args):
        arg = tuple(args)
        if args in mem:
            return mem[arg]
        res = fun(*args)
        mem[arg] = res
        return res
    return wraper

@memory
def partitions(n, k):
    if k < 2:
        return 1 if n in primes.primed else 0
    if k > n:
        return partitions(n, n)
    return partitions(n, k - 1) + partitions(n - k, k)

def p(n):
    return partitions(n, n)

print(p(10))
