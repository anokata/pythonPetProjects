#!/usr/bin/env python3
for x in range(1, 11):
    for y in range(1, 11):
        if x >= y:
            print("{} + {}; {}".format(x, y, x+y))
