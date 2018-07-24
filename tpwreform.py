#!/usr/bin/env python3
# 12 rolls
# for all - 12 * 0.02 * 4  = 0.96 96% max
# all single min - 12 * 0.03 = 36% min

base = 0
delta = int(input("enter delta: "))
k = 0.15
x = [base]

def next(xs):
    y = xs[-1] + (xs[-1] + delta) * k
    xs.append(round(y))

n = int(input("enter turns: "))
for i in range(n):
    next(x)
print(x)
