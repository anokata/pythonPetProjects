from itertools import permutations
from math import trunc, pow, floor
start = 1140
end = 1150
one_3 = 1./3.0

def is_cube(x):
    cube_root = pow(x, one_3)
    cu1 = floor(cube_root)
    cu3 = cu1 * cu1 * cu1
    return cu3 == x

def is_cube_perm(x):
    x = perm_to_float(x)
    return is_cube(x)

def perm_to_float(p):
    return float(''.join(p))

def perm():
    for i in range(start, end):
        cube = str(i**3)
        perms = permutations(cube)
        perms = list(set(perms))
        #perms = map(perm_to_float, perms)
        #perms = list(filter(is_cube, perms))
        perms = list(filter(is_cube_perm, perms))
        if len(perms) >= 3:
            print(i, len(perms))
            #print(perms)
#perm()
#test speed of ops
n = 1000000
import time
def timeit(fun, *args):
    def timer():
        t0 = time.time()
        fun(*args)
        t1 = time.time()
        return t1-t0
    return timer

@timeit
def test_pow1():
    for i in range(n):
        pass

@timeit
def test_pow2():
    a = 3
    b = 3.12
    for i in range(n):
        x = round(b)

@timeit
def test_pow3():
    a = 3
    b = 3.12
    for i in range(n):
        x = floor(b)

cold = test_pow1()
t1 = test_pow2()
t2 = test_pow3()
print(t1, t2)
