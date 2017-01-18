import random

n = random.randint(3, 5)
s = list()
for x in range(n):
    s.append(random.randint(1, 10))

print(s)

def solution(H):
    top = H[0]
    stk = [top]
    blk = 1
    for x in H:
        hei = 0
        if stk != []:
            hei = stk[-1]
        if hei > x:


        if x != top:
            blk += 1
            top = x
    return blk
