from typing import Dict
from typing import List

def a(bp): # type: (int) -> int
    x = list() # type: List[int]
    x.append(1)
    x.append(a(b('x')))
    return 1

def b(c): # type: (str) -> int
    return a(1)
