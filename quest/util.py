from mega import *

def join(sep, *args):
    return sep.join(args)

def Point(px, py):
    return DotDict(x=px, y=py)

#open result
OPEN_NEED_KEY = 1
OPEN_OPEND = 2
OPEN_CLOSED = 3
OPEN_CANNOT = 4
OPEN_NODOOR = 5
