#!/usr/bin/env python3
i = 1
for x in range(-10000, 10000):
    for y in range(-10000, 10000):
        if (abs(x)+abs(y)) < 100:
            i += 1

print(i)
