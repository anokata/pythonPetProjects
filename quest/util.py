from mega import *

def join(sep, *args):
    return sep.join(args)

def Point(px, py):
    return DotDict(x=px, y=py)
