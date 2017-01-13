  # 2
def solution_(N):
    nstr = str(bin(N)[2:])
    return max(map(len, nstr.split('1')))

def solution(N):
    nstr = str(bin(N)[2:])
    max_gap = 0
    current_gap = 0
    in_gap = False
    max_zero_in_half = len(nstr) // 2
    for i, c in enumerate(nstr):
        if in_gap:
            if c == "0":
                current_gap += 1
            else:
                in_gap = False
                if current_gap > max_gap:
                    max_gap = current_gap
                current_gap = 0
                if i >= max_zero_in_half and max_gap >= max_zero_in_half:
                    return max_gap
                    
        else:
            if c == "0":
                in_gap = True
                current_gap = 1
    if current_gap > max_gap:
        max_gap = current_gap
    return max_gap
    

import random
a = 0
for x in xrange(100000):
    a = solution_(random.randint(0, 2**30))
print a
