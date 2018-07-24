#!/usr/bin/env python3
import os

rows, columns = os.popen('stty size', 'r').read().split()

def pixelize_dot2(x, y):
    """ in: dot@(x, y) out terminal coord point """
    return (0, 0)
