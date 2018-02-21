#!/usr/bin/python3
import random
N = 8

def sumf(f):
    s = 0
    for row in f:
        for cell in row:
            s += cell

    return s

def randf():
    f = list()
    for x in range(8):
        f.append(list())
        for y in range(8):
            f[x].append(random.randint(0,1))
    return f

def neif(f, x, y):
    t = 1-f[x][y]
    n = 0
    if x > 0 and f[x-1][y] == t:
        n += 1
    if y > 0 and f[x][y-1] == t:
        n += 1
    if y < N-1 and f[x][y+1] == t:
        n += 1
    if x < N-1 and f[x+1][y] == t:
        n += 1
    return n


def is_okf(f):
    for x in range(8):
        for y in range(8):
            if neif(f, x, y) != 2:
                return False
    return True

def printf(f):
    for x in range(8):
        for y in range(8):
            print(f[x][y], end=" ")
        print(' ')

f = randf()
printf(f)
print(sumf(f))
print(neif(f,0,0))
print(neif(f,1,0))
print(neif(f,0,1))
print(neif(f,1,1))
print(is_okf(f))

while not is_okf(f):
    f = randf()

print(sumf(f))
print(is_okf(f))
printf(f)
