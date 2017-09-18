#!/usr/bin/env python3

def one(x, y):
    return x + y

def kon(x, y):
    return (x - y) * (x + y) - 1

def big(a, b, c):
    if not a:
        return 1
    if not b:
        return 2
    if not c:
        return 3
    x = a + b + c
    y = one(x, a * b * c)
    z = kon(x, y)
    return x + y + z

def safe(f):
    def _g(res, err, *args, **kwargs):
        if err:
            return (res, err)
        return f(*args, **kwargs)
    return _g

@safe
def fa(a):
    return 1

def big2(a, b, c):
    return fa(fa(a, 1, not a), 2, not b)

# global
iserr = False


print(big(1, 2, 3))
assert(big(1, 2, 3) == -91)
print(big2(1, 2, 3))
