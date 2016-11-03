from itertools import permutations
n = 10
l = ''.join([chr(x+48) for x in range(n)])
print(l)
all = permutations(l) 
nums = list()
sm = 0
for x in all:
    if x[0] != '0':
        n = ''.join(x)
        d2d4 = int(''.join(x[1:4]))
        if d2d4 % 2 != 0:
            continue
        
        if int(''.join(x[2:5])) % 3 != 0:
            continue
        if int(''.join(x[3:6])) % 5 != 0:
            continue
        if int(''.join(x[4:7])) % 7 != 0:
            continue
        if int(''.join(x[5:8])) % 11 != 0:
            continue
        if int(''.join(x[6:9])) % 13 != 0:
            continue
        if int(''.join(x[7:10])) % 17 != 0:
            continue

        #nums.append(int(n))
        sm += int(n)
#print(nums[:10], len(nums))
print(sm)
